from backend.config.settings import TOP_K
from backend.rag.vector_store import get_vector_store


def search_knowledge_base(question: str, k: int = TOP_K) -> list:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    vector_store = get_vector_store()
    return vector_store.similarity_search(question, k=k)


def print_results(question: str, k: int = TOP_K) -> None:
    results = search_knowledge_base(question, k=k)

    print(f"\nQuestion: {question}")
    print(f"Retrieved chunks: {len(results)}\n")

    for index, doc in enumerate(results, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page")
        page_label = page + 1 if isinstance(page, int) else "?"

        print(f"--- Result {index} ---")
        print(f"Source: {source} | Page: {page_label}")
        print(doc.page_content.strip())
        print()


def retrieve_context(question: str) -> dict:
    vector_store = get_vector_store()
    docs = vector_store.similarity_search(question, k=4)

    context_parts = []
    sources = []

    for doc in docs:
        context_parts.append(doc.page_content)

        sources.append({
            "document": doc.metadata.get("source", "unknown"),
            "page": doc.metadata.get("page", 0) + 1,
        })

    return {
        "context": "\n\n".join(context_parts),
        "sources": sources,
    }

if __name__ == "__main__":
    question = input("Ask a knowledge-base question: ")
    print_results(question)
