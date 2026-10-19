import asyncio
 
from fastapi import (
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

from backend.agents.orchestrator import builder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from backend.agents.orchestrator import graph
from backend.config.settings import GEMINI_MODEL
from backend.config.settings import POSTGRES_CHECKPOINT_URI
from backend.observability.phoenix_setup import tracer_provider
from backend.observability.phoenix_setup import tracer


# =========================================================
# Lifespan Event Handler    
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = AsyncConnectionPool(
        conninfo=POSTGRES_CHECKPOINT_URI,
        min_size=1,
        max_size=10,
        kwargs={
            "autocommit": True,
            "prepare_threshold": 0,
            "row_factory": dict_row,
        },
        open=False,
    )

    await pool.open()

    try:
        checkpointer = AsyncPostgresSaver(pool)
        await checkpointer.setup()

        app.state.db_pool = pool
        app.state.checkpointer = checkpointer
        app.state.graph = builder.compile(
            checkpointer=checkpointer
        )

        yield

    finally:
        await pool.close()


 
 
# =========================================================
# FastAPI Application
# =========================================================
 
app = FastAPI(
    title="BizInsight AI",
    description="Multi-Agent Business Intelligence Assistant",
    version="1.0.0",
    lifespan=lifespan,
)
 
 
# =========================================================
# CORS
# =========================================================
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
# =========================================================
# Request Schema
# =========================================================

class ChatRequest(BaseModel):
    question: str
 
 
# =========================================================
# Health Check
# =========================================================
 
@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "BizInsight AI",
    }
 
 
# =========================================================
# Normal HTTP Chat Endpoint
# =========================================================
 
@app.post("/chat")
def chat(request: ChatRequest):
 
    question = request.question.strip()
 
    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )
 
    try:
 
        initial_state = {
            "question": question,
            "logs": [],
        }

        with tracer.start_as_current_span("bizinsight.workflow") as span:
            
            span.set_attribute("input.question", question)

            result = graph.invoke(
                initial_state
            )

        sql_result = result.get("sql_result",{}) or {}
        rag_result = result.get("rag_result", {}) or {}
 
        return {

            "success": True,

            "question": question,
 
            "route": result.get(
                "route"
            ),
 
            "answer": result.get(
                "final_answer",
                "",
            ),
 
            "logs": result.get(
                "logs",
                []
            ),
 
            # ---------------------------------------------
            # SQL / MCP
            # ---------------------------------------------
 
            "sql": sql_result.get(
                "sql"
            ),
 
            "mcp_tool": sql_result.get(
                "mcp_tool"
            ),
 
            "database_rows": sql_result.get(
                "row_count",
                0
            ),
 
            "database_data": sql_result.get(
                "data",
                []
            ),
 
            # ---------------------------------------------
            # RAG
            # ---------------------------------------------
 
            "retrieved_documents": rag_result.get(
                "sources",
                []
            ),
 
            "rag_context": rag_result.get(
                "context",
                ""
            ),

        }
 
    except Exception as exc:
 
        raise HTTPException(
            status_code=500,
            detail=str(exc),

        ) from exc
 

@app.get("/chat/history/{thread_id}")
async def get_chat_history(thread_id: str):
    graph = app.state.graph

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    snapshot = await graph.aget_state(config)

    return {
        "thread_id": thread_id,
        "history": snapshot.values.get(
            "conversation_history", []
        ),
    }

from fastapi import HTTPException


@app.get("/chat/conversations")
async def get_conversations():
    graph = app.state.graph

    conversations = []
    seen_threads = set()

    try:
        async for checkpoint in graph.checkpointer.alist(None):
            config = checkpoint.config
            configurable = config.get("configurable", {})
            thread_id = configurable.get("thread_id")

            # Keep only the latest checkpoint for each thread.
            if not thread_id or thread_id in seen_threads:
                continue

            seen_threads.add(thread_id)

            values = checkpoint.checkpoint.get("channel_values", {})
            history = values.get("conversation_history", [])

            # Generate a title from the first question if available.
            title = "New conversation"

            if history:
                title = history[0].get(
                    "question", title
                )

            conversations.append({
                "thread_id": thread_id,
                "title": title,
            })

        return {"conversations": conversations}

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve conversations: {str(exc)}",
        ) from exc
 
# =========================================================
# WebSocket Chat Endpoint
# =========================================================
 
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket,):

    """
    Real-time LangGraph execution stream.
    Client sends:
        {
            "question": "..."
        }
 
    Server sends:
        - workflow_started
        - node_update
        - agent
        - logs
        - workflow_completed
        - error
    """
 
    await websocket.accept()

    graph = websocket.app.state.graph
 
    try:
        while True:
 
            # =================================================
            # Receive Request
            # =================================================
 
            request = await websocket.receive_json()

            import uuid 

            # thread_id = str(request.get("thread_id") or uuid.uuid4())
            thread_id = "Chakri_111"

            thread_id = str(request.get("thread_id") or uuid.uuid4())

            config = {
                "configurable": {
                    "thread_id": thread_id
                }
            }
 
            question = str(
                request.get(
                    "question",
                    ""
                )
            ).strip()

            model_provider = str(
                request.get(
                    "model_provider",
                    "gemini"
                )
            ).lower()

            model_name = str(
                request.get(
                    "model_name",
                    GEMINI_MODEL
                )
            ).strip()
 
            if not question:
                await websocket.send_json({
                    "type": "error",
                    "message": "Question cannot be empty.",
                })
                continue
 
            # =================================================
            # Workflow Started
            # =================================================
            await websocket.send_json({
                "type": "workflow_started",
                "thread_id": thread_id,
                "question": question,
            })
 
            # =================================================
            # Initial State
            # =================================================
 
            initial_state = {
                "question": question,
                "model_provider": model_provider,
                "model_name": model_name,
                "logs": [],
            }
 
            # -------------------------------------------------
            # IMPORTANT
            #
            # We maintain the state ourselves as LangGraph
            # sends updates.
            #
            # This prevents executing the graph twice.
            # -------------------------------------------------
 
            streamed_state = {
                **initial_state
            }
 
            # =================================================
            # Queue for Graph Events
            # =================================================
 
            queue = asyncio.Queue()
            loop = asyncio.get_running_loop()
 
            # =================================================
            # Run LangGraph in Worker Thread
            # =================================================
 
            def run_graph():

                # await websocket.send_json({
                #     "type": "agent_status",
                #     "agent": "orchestrator",
                #     "status": "running",
                # })
 
                try:
 
                    for update in graph.stream(
                        initial_state,
                        config=config,
                        stream_mode="updates",
                    ):
 
                        loop.call_soon_threadsafe(
                            queue.put_nowait,
                            {
                                "type": "graph_update",
                                "data": update,
                            },

                        )
 
                except Exception as exc:
                    loop.call_soon_threadsafe(
                        queue.put_nowait,
                        {
                            "type": "graph_error",
                            "message": str(exc),
                        },
                    )
                finally:
                    loop.call_soon_threadsafe(
                        queue.put_nowait,
                        {
                            "type": "graph_finished",
                        },
                    )

            graph_task = asyncio.create_task(

                asyncio.to_thread(
                    run_graph
                )
            )
 
 
            # =================================================
            # Process Graph Events
            # =================================================
 
            while True:
                event = await queue.get()
                event_type = event.get(
                    "type"
                )
 
                # -------------------------------------------------
                # Graph Error
                # -------------------------------------------------
 
                if event_type == "graph_error":
                    await websocket.send_json({
                        "type": "error",
                        "message": event.get(
                            "message",
                            "Graph execution failed.",
                        ),
                    })
                    continue
 
                # -------------------------------------------------
                # Graph Finished
                # -------------------------------------------------
 
                if event_type == "graph_finished":
                    break
 
                # -------------------------------------------------
                # Graph Node Update
                # -------------------------------------------------
 
                update = event.get(
                    "data",
                    {}
                )
 
                if not isinstance(

                    update,

                    dict

                ):

                    continue
 
 
                # -------------------------------------------------
                # IMPORTANT:
                #
                # Merge node output into our running state.
                # -------------------------------------------------
 
                streamed_state.update(
                    update
                )
 
                # -------------------------------------------------
                # Process every node update
                # -------------------------------------------------
 
                for node_name, node_data in update.items():
 
                    if not isinstance(node_data,dict):
                        node_data = {}
 
                    # ---------------------------------------------
                    # Send generic node update
                    # ---------------------------------------------
 
                    await websocket.send_json({

                        "type": "node_update",

                        "node": node_name,

                        "data": node_data,

                    })
 
 
                    # =================================================
                    # ORCHESTRATOR
                    # =================================================
 
                    if node_name == "orchestrator":
                        route = node_data.get(
                            "route"
                        )
 
                        await websocket.send_json({

                            "type": "agent",

                            "agent": "orchestrator",

                            "status": "completed",

                            "route": route,

                        })
 
 
                    # =================================================

                    # SQL AGENT

                    # =================================================
 
                    elif node_name == "sql_agent":
 
                        sql_result = node_data.get(

                            "sql_result",

                            {}

                        ) or {}
 
                        await websocket.send_json({

                            "type": "agent",
                            "agent": "sql_agent",
                            "status": "completed",
                            "sql": sql_result.get(
                                "sql"

                            ),

                            "mcp_tool": sql_result.get(

                                "mcp_tool"

                            ),

                            "database_rows": sql_result.get(

                                "row_count",

                                0

                            ),

                            "database_data": sql_result.get(

                                "data",

                                []

                            ),

                        })
 
 
                    # =================================================

                    # RAG AGENT

                    # =================================================
 
                    elif node_name == "rag_agent":
 
                        rag_result = node_data.get(

                            "rag_result",

                            {}

                        ) or {}
                        
                        
 
                        await websocket.send_json({

                            "type": "agent",

                            "agent": "rag_agent",

                            "status": "completed",

                            "sources": rag_result.get(

                                "sources",

                                []

                            ),

                            "document_count": rag_result.get(

                                "document_count",

                                0

                            ),

                            "context": rag_result.get(

                                "context",

                                ""

                            ),

                        })
 
 
                    # =================================================
                    # RESPONSE AGENT
                    # =================================================
 
                    elif node_name == "response_agent":
 
                        await websocket.send_json({

                            "type": "agent",

                            "agent": "response_agent",

                            "status": "completed",

                            "answer": node_data.get(

                                "final_answer",

                                ""

                            ),

                        })
 
 
                    # =================================================
                    # LOGS
                    # =================================================
 
                    logs = node_data.get(
                        "logs"
                    )
 
                    if logs:
 
                        await websocket.send_json({

                            "type": "logs",

                            "logs": logs,

                        })
 
 
            # =================================================
            # Wait for Graph Worker
            # =================================================
 
            await graph_task
 
 
            # =================================================
            # Build Final State
            # =================================================
 
            sql_result = streamed_state.get("sql_result", {}) or {}
            rag_result = streamed_state.get("rag_result", {}) or {}
 
 
            final_payload = {

                "type": "workflow_completed",

                "success": True,
 
                "question": question,
 
                "route": streamed_state.get("route"),
 
                "answer": streamed_state.get("final_answer", ""),
 
                "logs": streamed_state.get("logs", []),
 
                # ---------------------------------------------
                # SQL
                # ---------------------------------------------
 
                "sql": sql_result.get("sql"),
 
                "mcp_tool": sql_result.get("mcp_tool"),
 
                "database_rows": sql_result.get("row_count", 0),
 
                "database_data": sql_result.get("data", []),
 
                # ---------------------------------------------
                # RAG
                # ---------------------------------------------
 
                "retrieved_documents": rag_result.get("sources", []),
 
                "rag_context": rag_result.get("context", ""),

            }
 
            # =================================================
            # Send Final Result
            # =================================================
 
            await websocket.send_json(
                final_payload
            )
 
    except WebSocketDisconnect:
        print("WebSocket client disconnected.")
 
    except Exception as exc:

        print(f"WebSocket error: {exc}")
 
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(exc),
            })
        except Exception:
            pass
 
 
# =========================================================
# Run Directly
# =========================================================
 
if __name__ == "__main__":
 
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
 