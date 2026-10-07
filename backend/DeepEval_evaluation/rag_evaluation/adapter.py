import importlib
from typing import Any, Callable

from .config import RAG_RETRIEVER_IMPORT


def load_retriever() -> Callable[[str], Any]:
    """Dynamically load the existing BizInsight retrieve_context() function."""
    module_name, function_name = RAG_RETRIEVER_IMPORT.split(":", 1)
    module = importlib.import_module(module_name)
    retriever = getattr(module, function_name)
    if not callable(retriever):
        raise TypeError(f"{RAG_RETRIEVER_IMPORT} is not callable")
    return retriever


def _normalise_chunks(context: Any) -> list[str]:
    """Convert the existing retriever's context output into DeepEval's list[str]."""
    if context is None:
        return []

    if isinstance(context, list):
        return [str(x).strip() for x in context if str(x).strip()]

    text = str(context).strip()
    if not text:
        return []

    # Preferred fallback when the current retriever returns one joined string.
    chunks = [part.strip() for part in text.split("\n\n") if part.strip()]
    return chunks or [text]


def retrieve_for_eval(question: str) -> tuple[list[str], list[str]]:
    """
    Run the existing retriever and return:
        retrieval_context: list[str]
        sources: list[str]
    """
    retriever = load_retriever()
    result = retriever(question)

    if not isinstance(result, dict):
        raise TypeError(
            "retrieve_context() must return a dict containing at least 'context' "
            "and optionally 'sources'."
        )

    retrieval_context = _normalise_chunks(result.get("context", ""))
    sources = result.get("sources", []) or []
    sources = [str(source) for source in sources]

    return retrieval_context, sources
