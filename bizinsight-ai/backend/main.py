from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agents.orchestrator import graph


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="BizInsight AI",
    description="Multi-Agent Business Intelligence Assistant",
    version="1.0.0",
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
# Chat Endpoint
# =========================================================

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Send a business question through the LangGraph workflow.
    """

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

        # Run LangGraph
        result = graph.invoke(
            initial_state
        )

        # -------------------------------------------------
        # Extract SQL information
        # -------------------------------------------------

        sql_result = result.get(
            "sql_result",
            {}
        )

        sql = sql_result.get(
            "sql"
        )

        mcp_tool = sql_result.get(
            "mcp_tool"
        )

        database_data = sql_result.get(
            "data",
            []
        )

        database_rows = sql_result.get(
            "row_count",
            0
        )

        # -------------------------------------------------
        # Extract RAG information
        # -------------------------------------------------

        rag_result = result.get(
            "rag_result",
            {}
        )

        rag_sources = rag_result.get(
            "sources",
            []
        )

        rag_context = rag_result.get(
            "context",
            ""
        )

        # -------------------------------------------------
        # Final response
        # -------------------------------------------------

        return {
            "success": True,

            "question": question,

            "route": result.get(
                "route"
            ),

            "answer": result.get(
                "final_answer",
                "No answer generated.",
            ),

            "logs": result.get(
                "logs",
                []
            ),

            # SQL / MCP information
            "sql": sql,
            "mcp_tool": mcp_tool,
            "database_rows": database_rows,
            "database_data": database_data,

            # RAG information
            "retrieved_documents": rag_sources,
            "rag_context": rag_context,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


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