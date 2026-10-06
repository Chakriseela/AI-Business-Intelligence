from backend.rag.retriever import retrieve_context
from backend.observability.phoenix_setup import tracer


# =========================================================
# RAG Agent
# =========================================================

def rag_agent(
    question: str
) -> dict:

    with tracer.start_as_current_span("rag_agent") as span:
        """
        RAG Agent responsibilities:

        1. Search ChromaDB
        2. Retrieve relevant document chunks
        3. Return evidence + sources

        It does NOT generate the final answer.
        """

        span.set_attribute("agent.name", "rag_agent")
        span.set_attribute("input.question", question)

        with tracer.start_as_current_span("chroma.retrieval") as retrieval_span:

            retrieval_result = retrieve_context(
                question
            )

            context = retrieval_result.get(
                "context",
                ""
            )

            sources = retrieval_result.get(
                "sources",
                []
            )

            retrieval_span.set_attribute("retrieved.context_length", len(context))
            retrieval_span.set_attribute("retrieved.document_count", len(sources))

        span.set_attribute("rag.success", bool(context.strip()))
        span.set_attribute("rag.document_count", len(sources))

        return {
            "success": bool(
                context.strip()
            ),

            "context": context,

            "sources": sources,

            "document_count": len(
                sources
            ),
        }


# =========================================================
# Test
# =========================================================

if __name__ == "__main__":

    question = input(
        "Ask a knowledge-base question: "
    )

    result = rag_agent(
        question
    )

    print("\n" + "=" * 60)
    print("RAG AGENT")
    print("=" * 60)

    print("\nRetrieved Context:")
    print(
        result.get(
            "context",
            "No context found."
        )
    )

    print("\nSources:")

    for source in result.get(
        "sources",
        []
    ):

        print(
            f"- {source.get('document')} "
            f"(Page {source.get('page')})"
        )