import csv
import json
import sys
from pathlib import Path

from google import genai
from deepeval import evaluate
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
)
from deepeval.test_case import LLMTestCase

# Make the BizInsight project importable when this file is run from its folder.
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.DeepEval_evaluation.rag_evaluation.adapter import retrieve_for_eval
from backend.DeepEval_evaluation.rag_evaluation.config import DATASET_FILE, EVAL_MODEL, RESULTS_DIR


# Judge model used by DeepEval metrics.
metrics = [
    ContextualRelevancyMetric(
        threshold=0.70,
        model=EVAL_MODEL,
        include_reason=True,
    ),
    ContextualPrecisionMetric(
        threshold=0.70,
        model=EVAL_MODEL,
        include_reason=True,
    ),
    ContextualRecallMetric(
        threshold=0.70,
        model=EVAL_MODEL,
        include_reason=True,
    ),
]


client = genai.Client()


def generate_answer(question: str, retrieval_context: list[str]) -> str:
    """Generate an answer only so reference-based retrieval metrics have actual_output."""
    context = "\n\n".join(retrieval_context)
    prompt = f"""
Answer the user's question using only the supplied context.
Do not add facts that are not present in the context.

Question:
{question}

Context:
{context}
""".strip()

    response = client.models.generate_content(
        model=EVAL_MODEL,
        contents=prompt,
    )
    return (response.text or "").strip()


def load_cases() -> list[dict[str, str]]:
    with DATASET_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_test_cases() -> list[LLMTestCase]:
    test_cases: list[LLMTestCase] = []

    for row in load_cases():
        case_id = row["id"].strip()
        question = row["question"].strip()
        expected_output = row["expected_output"].strip()

        if not question or question.startswith("Replace with"):
            print(f"Skipping {case_id}: replace the placeholder question first.")
            continue

        if not expected_output or expected_output.startswith("Replace with"):
            print(f"Skipping {case_id}: replace the placeholder expected answer first.")
            continue

        print("=" * 80)
        print(f"TEST CASE: {case_id}")
        print(f"Question: {question}")

        retrieval_context, sources = retrieve_for_eval(question)
        print(f"Retrieved chunks: {len(retrieval_context)}")
        print(f"Sources: {sources}")

        actual_output = generate_answer(question, retrieval_context)
        print(f"Generated answer: {actual_output}")

        test_cases.append(
            LLMTestCase(
                input=question,
                actual_output=actual_output,
                expected_output=expected_output,
                retrieval_context=retrieval_context,
            )
        )

    return test_cases


def save_summary(test_cases_count: int) -> None:
    summary = {
        "test_cases": test_cases_count,
        "metrics": [
            "ContextualRelevancyMetric",
            "ContextualPrecisionMetric",
            "ContextualRecallMetric",
        ],
        "threshold": 0.70,
        "model": EVAL_MODEL,
    }
    output_file = RESULTS_DIR / "rag_evaluation_config.json"
    output_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nConfiguration written to: {output_file}")


def main() -> None:
    test_cases = build_test_cases()

    if not test_cases:
        raise RuntimeError(
            "No valid test cases found. Fill datasets/rag_test_cases.csv first."
        )

    print("\n" + "=" * 80)
    print("STARTING BIZINSIGHT DEEPEVAL RAG RETRIEVAL EVALUATION")
    print("=" * 80)
    print(f"Dataset size: {len(test_cases)}")
    print(f"Evaluation model: {EVAL_MODEL}")

    evaluate(
        test_cases=test_cases,
        metrics=metrics,
    )

    save_summary(len(test_cases))


if __name__ == "__main__":
    main()
