from typing import TypedDict, Literal
import asyncio
import ollama
 
from google import genai
from langgraph.graph import StateGraph, START, END
 
from backend.config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    OLLAMA_MODEL
)
 
from backend.agents.sql_agent import sql_agent
from backend.agents.rag_agent import rag_agent
from backend.agents.response_agent import response_agent
from backend.LLM_Models.llm_responce_generator import generate_with_selected_model
from backend.Prompts.agent_decision_prompt import get_orchestrator_prompt
from backend.observability.phoenix_setup import tracer
 
 
# =========================================================
# Gemini Client
# =========================================================
 
client = genai.Client(
    api_key=GEMINI_API_KEY
)
 
 
# =========================================================
# Graph State
# =========================================================
 
class AgentState(TypedDict, total=False):
    question: str
    route: str

    model_provider: str
    model_name: str
 
    sql_result: dict
    rag_result: dict
 
    final_answer: str
    logs: list[str]
 
 
# =========================================================
# Helper: Add Log
# =========================================================
 
def add_log(
    state: AgentState,
    message: str
) -> list[str]:
 
    logs = state.get("logs", []).copy()
    logs.append(message)
 
    return logs
 
 
# =========================================================
# 1. ORCHESTRATOR AGENT
# =========================================================
 
def orchestrator(state: AgentState) -> dict:

    with tracer.start_as_current_span("orchestrator") as span:
        """
        Decide whether the question requires:
    
        SQL
        RAG
        BOTH
        """
        question = state["question"]

        span.set_attribute("agent.name", "orchestrator")
        span.set_attribute("input.question", question)
        
        logs = add_log(
            state,
            "Orchestrator started"
        )
    
        prompt = get_orchestrator_prompt(question)

        provider = state.get(
            "model_provider",
            "gemini"
        )
        
        model_name = state.get(
            "model_name",
            GEMINI_MODEL
        )

        span.set_attribute("llm.provider", provider)
        span.set_attribute("llm.model", model_name)

        model_response = generate_with_selected_model(
            prompt,
            provider,
            model_name,

        )
    
        route = model_response.upper().strip()
    

        # try:
    
        #         response = client.models.generate_content(
        #             model=GEMINI_MODEL,
        #             contents=prompt,
        #             # config=GENERATION_CONFIG,
        #         )
        #         model = "GEMINI MODEL"
        #         response = response.text.strip()
    
    
        # except Exception:
        #     response = ollama.chat(
        #         model=OLLAMA_MODEL,
        #         messages=[
        #             {
        #                 "role": "user",
        #                 "content": prompt,
        #             }
        #         ],
        #     )
        #     model = "OLLAMA qwen3.5:0.8b"
        #     response = response["message"]["content"].strip()
        # route = response 
    
        logs = add_log(
                state,
                f"orchestrator llm {model_name} selected: {route}"
            )
    
        logs.append(
            f"MODEL selected: {provider} {model_name}"
        )
    
        logs.append(
            f"MODEL selected: {route}"
        )
    
        # Remove accidental markdown
        route = (
            route
            .replace("```", "")
            .replace("\n", " ")
            .strip()
            .upper()
        )
    
        # Safety fallback
        if route not in {"SQL", "RAG", "BOTH"}:
            route = "RAG"

        span.set_attribute("orchestrator.route", route)
    
        logs = add_log(
            state,
            f"Orchestrator selected: {route}"
        )
    
        return {
            "route": route,
            "logs": logs,
        }
 
 
# =========================================================
# 2. SQL AGENT NODE
# =========================================================
 
def sql_agent_node(state: AgentState) -> dict:
 
    question = state["question"]
 
    logs = add_log(
        state,
        "SQL Agent started"
    )
 
    try:
        # result = asyncio.run(
        #     sql_agent(question)
        # )
        result = asyncio.run(
            sql_agent(
                question=question,
                model_provider=state.get(
                    "model_provider",
                    "gemini"
                ),
                model_name=state.get(
                    "model_name",
                    GEMINI_MODEL
                ),
            )
        )
        logs.append(
            "SQL query execution completed"
        )
 
    except Exception as exc:
 
        logs.append(
            f"SQL Agent failed: {exc}"
        )
 
        return {
            "sql_result": {
                "success": False,
                "data": [],
                "error": str(exc),
            },
            "logs": logs,
        }
 
    logs.append(
        "SQL Agent completed"
    )
 
    if result.get("mcp_tool"):
 
        logs.append(
            f"MCP Tool used: "
            f"{result['mcp_tool']}"
        )
 
    if result.get("sql"):
 
        logs.append(
            f"Generated SQL: "
            f"{result['sql']}"
        )
 
    logs.append(
        f"Database rows returned: "
        f"{result.get('row_count', 0)}"
    )
 
    return {
        "sql_result": result,
        "logs": logs,
    }
 
 
# =========================================================
# 3. RAG AGENT NODE
# =========================================================
 
def rag_agent_node(state: AgentState) -> dict:
 
    question = state["question"]
 
    logs = add_log(
        state,
        "RAG Agent started"
    )
 
    try:
        result = rag_agent(question)
        logs.append(
            "ChromaDB retrieval completed"
        )
 
    except Exception as exc:
 
        logs.append(
            f"RAG Agent failed: {exc}"
        )
 
        return {
            "rag_result": {
                "success": False,
                "context": "",
                "sources": [],
                "error": str(exc),
            },
            "logs": logs,
        }
 
    logs.append(
        "RAG Agent completed"
    )
 
    logs.append(
        f"RAG documents retrieved: "
        f"{result.get('document_count', 0)}"
    )
 
    for source in result.get(
        "sources",
        []
    ):
 
        logs.append(
            f"RAG Source: "
            f"{source.get('document', 'unknown')}, "
            f"Page {source.get('page', 'unknown')}"
        )
 
    return {
        "rag_result": result,
        "logs": logs,
    }
 
 
# =========================================================
# 4. RESPONSE AGENT NODE
# =========================================================
 
def response_agent_node(state: AgentState) -> dict:
    """
    Combine SQL and/or RAG results into the final answer.
    """
 
    logs = add_log(
        state,
        "Response Agent started"
    )
 
    try:
 
        answer = response_agent(
            question=state["question"],
            sql_result=state.get("sql_result"),
            rag_result=state.get("rag_result"),
            model_provider=state.get(
                "model_provider",
                "gemini"
            ),
            model_name=state.get(
                "model_name",
                GEMINI_MODEL
            ),
        )
 
    except Exception as exc:
 
        logs.append(
            f"Response Agent failed: {exc}"
        )
 
        return {
            "final_answer": (
                "I was unable to generate the final response."
            ),
            "logs": logs,
        }
 
    logs.append(
        "Response Agent completed"
    )
 
    return {
        "final_answer": answer,
        "logs": logs,
    }
 
 
# =========================================================
# 5. ROUTING AFTER ORCHESTRATOR
# =========================================================
 
def route_after_orchestrator(
    state: AgentState,
) -> Literal[
    "sql_agent",
    "rag_agent",
]:
    """
    Decide the first specialist node.
 
    SQL -> SQL Agent
    RAG -> RAG Agent
    BOTH -> SQL Agent first
 
    For BOTH, after SQL we route to RAG.
    """
 
    route = state.get("route", "RAG")
 
    if route == "SQL":
        return "sql_agent"
 
    if route == "RAG":
        return "rag_agent"
 
    # BOTH
    return "sql_agent"
 
 
# =========================================================
# 6. ROUTING AFTER SQL AGENT
# =========================================================
 
def route_after_sql(
    state: AgentState,
) -> Literal[
    "rag_agent",
    "response_agent",
]:
    """
    Decide what happens after SQL Agent.
 
    SQL  -> Response Agent
    BOTH -> RAG Agent
    """
 
    route = state.get("route", "SQL")
 
    if route == "BOTH":
        return "rag_agent"
 
    return "response_agent"
 
 
# =========================================================
# 7. BUILD LANGGRAPH
# =========================================================
 
builder = StateGraph(
    AgentState
)
 
 
# =========================================================
# Add Nodes
# =========================================================
 
builder.add_node(
    "orchestrator",
    orchestrator,
)
 
builder.add_node(
    "sql_agent",
    sql_agent_node,
)
 
builder.add_node(
    "rag_agent",
    rag_agent_node,
)
 
builder.add_node(
    "response_agent",
    response_agent_node,
)
 
 
# =========================================================
# START -> ORCHESTRATOR
# =========================================================
 
builder.add_edge(
    START,
    "orchestrator",
)
 
 
# =========================================================
# ORCHESTRATOR -> SQL / RAG
# =========================================================
 
builder.add_conditional_edges(
    "orchestrator",
    route_after_orchestrator,
    {
        "sql_agent": "sql_agent",
        "rag_agent": "rag_agent",
    },
)
 
 
# =========================================================
# SQL -> RAG or RESPONSE
# =========================================================
 
builder.add_conditional_edges(
    "sql_agent",
    route_after_sql,
    {
        "rag_agent": "rag_agent",
        "response_agent": "response_agent",
    },
)
 
 
# =========================================================
# RAG -> RESPONSE
# =========================================================
 
builder.add_edge(
    "rag_agent",
    "response_agent",
)
 
 
# =========================================================
# RESPONSE -> END
# =========================================================
 
builder.add_edge(
    "response_agent",
    END,
)
 
 
# =========================================================
# COMPILE
# =========================================================
 
graph = builder.compile()
 
 
# =========================================================
# RUN GRAPH
# =========================================================
 
def run(question: str):
 
    initial_state: AgentState = {
        "question": question,
        "model_provider": "gemini",
        "model_name": GEMINI_MODEL,
        "logs": [],
    }
 
    result = graph.invoke(
        initial_state
    )
 
    print("\n")
    print("=" * 70)
    print("BIZINSIGHT AI")
    print("=" * 70)
 
    print("\nQuestion:")
    print(question)
 
    print("\nRoute:")
    print(result.get("route"))
 
    print("\nExecution Logs:")
    print("-" * 70)
 
    for log in result.get(
        "logs",
        []
    ):
        print(f"• {log}")
 
    print("\nFinal Answer:")
    print("-" * 70)
 
    print(
        result.get(
            "final_answer",
            "No answer generated."
        )
    )
 
    print("\n")
 
    return result
 
 
# =========================================================
# MAIN
# =========================================================
 
if __name__ == "__main__":
 
    question = input(
        "Ask a business question: "
    )
 
    run(question)