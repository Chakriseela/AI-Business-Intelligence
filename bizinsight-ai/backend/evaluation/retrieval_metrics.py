from typing import Any


# =========================================================
# Normalize document name
# =========================================================

def normalize_document_name(document: str) -> str:
    """
    Normalize a document filename for reliable comparison.
    """

    return str(document).strip().lower()


# =========================================================
# Extract document names from RAG sources
# =========================================================

def get_retrieved_documents(
    sources: list[dict[str, Any]],
) -> list[str]:
    """
    Extract document filenames from the sources returned
    by the RAG retriever.

    Example input:

    [
        {"document": "warranty_policy.pdf", "page": 1},
        {"document": "faq.pdf", "page": 1}
    ]

    Returns:

    [
        "warranty_policy.pdf",
        "faq.pdf"
    ]
    """

    documents = []

    for source in sources:

        if not isinstance(source, dict):
            continue

        document = source.get(
            "document",
            "",
        )

        if document:

            documents.append(
                normalize_document_name(
                    document
                )
            )

    return documents


# =========================================================
# Hit Rate @ K
# =========================================================

def hit_rate_at_k(
    retrieved_documents: list[str],
    expected_document: str,
    k: int = 3,
) -> float:
    """
    Hit Rate@K checks whether the expected document
    appears anywhere in the top-K retrieved documents.

    Result:
        1.0 -> found
        0.0 -> not found
    """

    expected_document = normalize_document_name(
        expected_document
    )

    top_k = retrieved_documents[:k]

    return float(
        expected_document in top_k
    )


# =========================================================
# Precision @ K
# =========================================================

def precision_at_k(
    retrieved_documents: list[str],
    expected_document: str,
    k: int = 3,
) -> float:
    """
    Document-level Precision@K.

    Since this evaluation dataset currently defines
    one expected relevant document per question,
    Precision@K is:

        relevant retrieved results / retrieved results
        in top-K
    """

    expected_document = normalize_document_name(
        expected_document
    )

    top_k = retrieved_documents[:k]

    if not top_k:
        return 0.0

    relevant_count = sum(
        1
        for document in top_k
        if document == expected_document
    )

    return relevant_count / len(top_k)


# =========================================================
# Recall @ K
# =========================================================

def recall_at_k(
    retrieved_documents: list[str],
    expected_document: str,
    k: int = 3,
) -> float:
    """
    Document-level Recall@K.

    Because the current dataset has one expected
    relevant document per question:

        1.0 -> expected document retrieved
        0.0 -> expected document not retrieved
    """

    expected_document = normalize_document_name(
        expected_document
    )

    top_k = retrieved_documents[:k]

    return float(
        expected_document in top_k
    )


# =========================================================
# Reciprocal Rank
# =========================================================

def reciprocal_rank(
    retrieved_documents: list[str],
    expected_document: str,
) -> float:
    """
    Reciprocal Rank:

        1 / rank

    Example:

        expected document at rank 1 -> 1.00
        expected document at rank 2 -> 0.50
        expected document at rank 3 -> 0.33

    If the expected document is not found:

        0.00
    """

    expected_document = normalize_document_name(
        expected_document
    )

    for rank, document in enumerate(
        retrieved_documents,
        start=1,
    ):

        if document == expected_document:

            return 1.0 / rank

    return 0.0


# =========================================================
# Evaluate one retrieval result
# =========================================================

def evaluate_retrieval(
    sources: list[dict[str, Any]],
    expected_document: str,
    k: int = 3,
) -> dict[str, Any]:
    """
    Calculate all retrieval metrics for one test case.
    """

    retrieved_documents = (
        get_retrieved_documents(
            sources
        )
    )

    return {
        "expected_document":
            normalize_document_name(
                expected_document
            ),

        "retrieved_documents":
            retrieved_documents,

        "k":
            k,

        "hit_rate_at_k":
            hit_rate_at_k(
                retrieved_documents,
                expected_document,
                k,
            ),

        "precision_at_k":
            precision_at_k(
                retrieved_documents,
                expected_document,
                k,
            ),

        "recall_at_k":
            recall_at_k(
                retrieved_documents,
                expected_document,
                k,
            ),

        "mrr":
            reciprocal_rank(
                retrieved_documents,
                expected_document,
            ),
    }


# =========================================================
# Average metrics across the complete dataset
# =========================================================

def average_retrieval_metrics(
    results: list[dict[str, Any]],
) -> dict[str, float]:
    """
    Calculate average retrieval metrics across
    all successful test cases.
    """

    if not results:
        return {
            "hit_rate_at_k": 0.0,
            "precision_at_k": 0.0,
            "recall_at_k": 0.0,
            "mrr": 0.0,
        }

    count = len(results)

    return {
        "hit_rate_at_k": (
            sum(
                result["hit_rate_at_k"]
                for result in results
            ) / count
        ),

        "precision_at_k": (
            sum(
                result["precision_at_k"]
                for result in results
            ) / count
        ),

        "recall_at_k": (
            sum(
                result["recall_at_k"]
                for result in results
            ) / count
        ),

        "mrr": (
            sum(
                result["mrr"]
                for result in results
            ) / count
        ),
    }