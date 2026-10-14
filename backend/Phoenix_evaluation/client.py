import time

from backend.agents.orchestrator import graph


# ==========================================
# BIZINSIGHT APPLICATION CLIENT
# ==========================================

def ask(question: str) -> dict:
    """
    Execute the existing BizInsight AI workflow.

    This function is called by Phoenix
    for every dataset example.
    """

    start_time = time.perf_counter()

    # --------------------------------------
    # EXECUTE EXISTING WORKFLOW
    # --------------------------------------

    result = graph.invoke({
            "question": question
        })

    # --------------------------------------
    # MEASURE LATENCY
    # --------------------------------------

    latency = time.perf_counter() - start_time

    # --------------------------------------
    # VALIDATE RESPONSE
    # --------------------------------------

    if not isinstance(result, dict):
        raise TypeError(
            "BizInsight workflow must return a dictionary."
        )

    final_answer = result.get(
        "final_answer",
        ""
    )

    if not isinstance(final_answer, str):
        final_answer = str(final_answer)

    if not final_answer.strip():
        raise ValueError(
            "BizInsight workflow returned an empty answer."
        )

    # --------------------------------------
    # EXTRACT METADATA
    # --------------------------------------

    route = result.get(
        "route",
        "unknown"
    )

    sources = result.get(
        "sources",
        []
    )

    if sources is None:
        sources = []

    # --------------------------------------
    # RETURN STRUCTURED OUTPUT
    # --------------------------------------

    return {
        "question": question,
        "answer": final_answer,
        "route": str(route),
        "sources": sources,
        "latency": round(latency, 3),
        "context": result.get("context", "")
    }
