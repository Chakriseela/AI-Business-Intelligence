import time

from backend.agents.orchestrator import graph


def ask(question: str) -> dict:
    """
    Executes the BizInsight workflow.

    Returns:
        {
            question,
            answer,
            latency,
            route,
            sources
        }
    """

    start = time.perf_counter()

    result = graph.invoke({
        "question": question
    })

    latency = time.perf_counter() - start

    return {
        "question": question,
        "answer": result.get("final_answer", ""),
        "route": result.get("route", ""),
        "sources": result.get("sources", []),
        "latency": round(latency, 3),
    }
