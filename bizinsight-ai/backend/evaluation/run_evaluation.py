import csv
import json
from pathlib import Path
from datetime import datetime

from backend.agents.rag_agent import rag_agent
from backend.evaluation.dataset import EVALUATION_DATASET

from backend.evaluation.retrieval_metrics import (
    evaluate_retrieval,
    average_retrieval_metrics,
)


# =========================================================
# Configuration
# =========================================================

K = 5

RESULTS_DIR = (
    Path(__file__).resolve().parent
    / "results"
)


# =========================================================
# Ensure results directory exists
# =========================================================

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# Format percentage
# =========================================================

def percentage(value: float) -> str:
    return f"{value * 100:.2f}%"


# =========================================================
# Evaluate one test case
# =========================================================

def evaluate_single_case(
    test_case: dict,
) -> dict:

    test_id = test_case["id"]

    question = test_case["question"]

    expected_document = (
        test_case["expected_document"]
    )

    print("\n" + "=" * 80)

    print(
        f"TEST CASE: {test_id}"
    )

    print("=" * 80)

    print(
        f"\nQuestion:\n{question}"
    )

    print(
        f"\nExpected Document:\n"
        f"{expected_document}"
    )

    # -----------------------------------------------------
    # Run actual BizInsight RAG
    # -----------------------------------------------------

    try:

        rag_result = rag_agent(
            question
        )

    except Exception as exc:

        print(
            f"\nRAG execution failed: {exc}"
        )

        return {
            "id": test_id,
            "question": question,
            "expected_document": (
                expected_document
            ),
            "retrieved_documents": [],
            "k": K,
            "hit_rate_at_k": 0.0,
            "precision_at_k": 0.0,
            "recall_at_k": 0.0,
            "mrr": 0.0,
            "success": False,
            "error": str(exc),
        }

    # -----------------------------------------------------
    # Get sources
    # -----------------------------------------------------

    sources = rag_result.get(
        "sources",
        [],
    ) or []

    # -----------------------------------------------------
    # Calculate deterministic metrics
    # -----------------------------------------------------

    metrics = evaluate_retrieval(
        sources=sources,
        expected_document=expected_document,
        k=K,
    )

    # -----------------------------------------------------
    # Display retrieved documents
    # -----------------------------------------------------

    print(
        "\nRetrieved Documents:"
    )

    for rank, document in enumerate(
        metrics["retrieved_documents"],
        start=1,
    ):

        print(
            f"  {rank}. {document}"
        )

    # -----------------------------------------------------
    # Display metrics
    # -----------------------------------------------------

    print(
        "\nMetrics:"
    )

    print(
        f"  Hit Rate@{K}    : "
        f"{percentage(metrics['hit_rate_at_k'])}"
    )

    print(
        f"  Precision@{K}  : "
        f"{percentage(metrics['precision_at_k'])}"
    )

    print(
        f"  Recall@{K}     : "
        f"{percentage(metrics['recall_at_k'])}"
    )

    print(
        f"  MRR            : "
        f"{metrics['mrr']:.4f}"
    )

    # -----------------------------------------------------
    # Build complete result
    # -----------------------------------------------------

    return {
        "id": test_id,

        "question": question,

        "expected_answer":
            test_case.get(
                "expected_answer",
                "",
            ),

        "expected_document":
            expected_document,

        "retrieved_documents":
            metrics["retrieved_documents"],

        "k":
            K,

        "hit_rate_at_k":
            metrics["hit_rate_at_k"],

        "precision_at_k":
            metrics["precision_at_k"],

        "recall_at_k":
            metrics["recall_at_k"],

        "mrr":
            metrics["mrr"],

        "retrieved_document_count":
            len(
                metrics[
                    "retrieved_documents"
                ]
            ),

        "success": True,
    }


# =========================================================
# Save JSON report
# =========================================================

def save_json_report(
    results: list[dict],
    summary: dict,
) -> Path:

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        RESULTS_DIR
        / f"retrieval_evaluation_{timestamp}.json"
    )

    report = {
        "evaluation": {
            "project": "BizInsight AI",
            "type": "Deterministic RAG Retrieval Evaluation",
            "k": K,
            "timestamp": timestamp,
        },

        "summary": summary,

        "test_cases": results,
    }

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
        )

    return output_file


# =========================================================
# Save CSV report
# =========================================================

def save_csv_report(
    results: list[dict],
) -> Path:

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        RESULTS_DIR
        / f"retrieval_evaluation_{timestamp}.csv"
    )

    fieldnames = [
        "id",
        "question",
        "expected_document",
        "retrieved_documents",
        "hit_rate_at_k",
        "precision_at_k",
        "recall_at_k",
        "mrr",
        "success",
        "error",
    ]

    with output_file.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for result in results:

            writer.writerow({
                "id":
                    result.get("id", ""),

                "question":
                    result.get(
                        "question",
                        "",
                    ),

                "expected_document":
                    result.get(
                        "expected_document",
                        "",
                    ),

                "retrieved_documents":
                    " | ".join(
                        result.get(
                            "retrieved_documents",
                            [],
                        )
                    ),

                "hit_rate_at_k":
                    result.get(
                        "hit_rate_at_k",
                        0.0,
                    ),

                "precision_at_k":
                    result.get(
                        "precision_at_k",
                        0.0,
                    ),

                "recall_at_k":
                    result.get(
                        "recall_at_k",
                        0.0,
                    ),

                "mrr":
                    result.get(
                        "mrr",
                        0.0,
                    ),

                "success":
                    result.get(
                        "success",
                        False,
                    ),

                "error":
                    result.get(
                        "error",
                        "",
                    ),
            })

    return output_file


# =========================================================
# Print complete summary
# =========================================================

def print_summary(
    results: list[dict],
    summary: dict,
) -> None:

    successful = [
        result
        for result in results
        if result.get("success")
    ]

    failed = [
        result
        for result in results
        if not result.get("success")
    ]

    print("\n\n")

    print("=" * 80)
    print("BIZINSIGHT AI")
    print("RAG RETRIEVAL EVALUATION REPORT")
    print("=" * 80)

    print(
        f"\nTotal Test Cases : "
        f"{len(results)}"
    )

    print(
        f"Successful        : "
        f"{len(successful)}"
    )

    print(
        f"Failed            : "
        f"{len(failed)}"
    )

    print(
        f"Top-K             : "
        f"{K}"
    )

    print("\n" + "-" * 80)
    print("AVERAGE METRICS")
    print("-" * 80)

    print(
        f"\nHit Rate@{K}    : "
        f"{percentage(summary['hit_rate_at_k'])}"
    )

    print(
        f"Precision@{K}  : "
        f"{percentage(summary['precision_at_k'])}"
    )

    print(
        f"Recall@{K}     : "
        f"{percentage(summary['recall_at_k'])}"
    )

    print(
        f"MRR            : "
        f"{summary['mrr']:.4f}"
    )

    print("\n" + "-" * 80)
    print("TEST CASE RESULTS")
    print("-" * 80)

    print(
        f"\n{'ID':<12}"
        f"{'Hit@K':<12}"
        f"{'Precision':<14}"
        f"{'Recall':<12}"
        f"{'MRR':<10}"
    )

    print("-" * 60)

    for result in results:

        print(
            f"{result.get('id', ''):<12}"
            f"{percentage(result.get('hit_rate_at_k', 0.0)):<12}"
            f"{percentage(result.get('precision_at_k', 0.0)):<14}"
            f"{percentage(result.get('recall_at_k', 0.0)):<12}"
            f"{result.get('mrr', 0.0):<10.4f}"
        )

    print("\n" + "=" * 80)


# =========================================================
# Main evaluation
# =========================================================

def run_evaluation():

    print("\n")
    print("=" * 80)
    print("STARTING BIZINSIGHT RAG RETRIEVAL EVALUATION")
    print("=" * 80)

    print(
        f"\nDataset size: "
        f"{len(EVALUATION_DATASET)}"
    )

    print(
        f"Evaluating Top-K: {K}"
    )

    results = []

    # -----------------------------------------------------
    # Run every test case
    # -----------------------------------------------------

    for test_case in EVALUATION_DATASET:

        result = evaluate_single_case(
            test_case
        )

        results.append(
            result
        )

    # -----------------------------------------------------
    # Successful results only
    # -----------------------------------------------------

    successful_results = [
        result
        for result in results
        if result.get("success")
    ]

    # -----------------------------------------------------
    # Calculate average metrics
    # -----------------------------------------------------

    summary = average_retrieval_metrics(
        successful_results
    )

    # -----------------------------------------------------
    # Print report
    # -----------------------------------------------------

    print_summary(
        results,
        summary,
    )

    # -----------------------------------------------------
    # Save reports
    # -----------------------------------------------------

    json_file = save_json_report(
        results,
        summary,
    )

    csv_file = save_csv_report(
        results
    )

    print(
        "\nJSON report saved to:"
    )

    print(
        json_file
    )

    print(
        "\nCSV report saved to:"
    )

    print(
        csv_file
    )


# =========================================================
# Entry point
# =========================================================

if __name__ == "__main__":

    run_evaluation()