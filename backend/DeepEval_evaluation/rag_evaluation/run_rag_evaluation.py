import os
import csv
import json
from pathlib import Path

from dotenv import load_dotenv

from deepeval import evaluate
from deepeval.models import GeminiModel
from deepeval.metrics import (
    ContextualRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)
from deepeval.test_case import LLMTestCase

from backend.agents.rag_agent import rag_agent
from backend.agents.response_agent import response_agent


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# 2. API KEY
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured in the environment."
    )


# ============================================================
# 3. PATHS
# ============================================================

# Current file:
#
# backend/
#   DeepEval_evaluation/
#       rag_evaluation/
#           run_rag_evaluation.py
#
# parents[0] = rag_evaluation
# parents[1] = DeepEval_evaluation
# parents[2] = backend
# parents[3] = project root

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATASET_PATH = (
    PROJECT_ROOT
    / "backend"
    / "DeepEval_evaluation"
    / "datasets"
    / "rag_test_cases.csv"
)

RESULTS_DIR = (
    PROJECT_ROOT
    / "backend"
    / "DeepEval_evaluation"
    / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 4. GEMINI EVALUATION MODEL
# ============================================================

EVAL_MODEL_NAME = os.getenv(
    "DEEPEVAL_MODEL",
    "gemini-2.5-flash"
)

eval_model = GeminiModel(
    model=EVAL_MODEL_NAME,
    api_key=GEMINI_API_KEY,
    temperature=0,
)


# ============================================================
# 5. DEEPEVAL METRICS
# ============================================================

contextual_relevancy = ContextualRelevancyMetric(
    threshold=0.70,
    model=eval_model,
    include_reason=True,
)

contextual_precision = ContextualPrecisionMetric(
    threshold=0.70,
    model=eval_model,
    include_reason=True,
)

contextual_recall = ContextualRecallMetric(
    threshold=0.70,
    model=eval_model,
    include_reason=True,
)


METRICS = [
    contextual_relevancy,
    contextual_precision,
    contextual_recall,
]


# ============================================================
# 6. LOAD CSV DATASET
# ============================================================

def load_test_cases() -> list[dict]:

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"Dataset not found:\n{DATASET_PATH}"
        )

    test_cases = []

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        required_columns = {
            "id",
            "question",
            "expected_output",
        }

        actual_columns = set(
            reader.fieldnames or []
        )

        missing_columns = (
            required_columns
            - actual_columns
        )

        if missing_columns:

            raise ValueError(
                "CSV is missing required columns: "
                f"{sorted(missing_columns)}"
            )

        for row in reader:

            test_cases.append(
                {
                    "id": (
                        row["id"] or ""
                    ).strip(),

                    "question": (
                        row["question"] or ""
                    ).strip(),

                    "expected_output": (
                        row["expected_output"] or ""
                    ).strip(),
                }
            )

    return test_cases


# ============================================================
# 7. CONVERT RAG CONTEXT
# ============================================================

def get_retrieval_context(
    rag_result: dict
) -> list[str]:

    context = rag_result.get(
        "context",
        ""
    )

    # --------------------------------------------------------
    # Case 1:
    # Your future/current retriever may return a list
    # --------------------------------------------------------

    if isinstance(context, list):

        return [
            str(chunk).strip()
            for chunk in context
            if str(chunk).strip()
        ]

    # --------------------------------------------------------
    # Case 2:
    # Your current rag_agent returns a string
    # --------------------------------------------------------

    if isinstance(context, str):

        context = context.strip()

        if context:

            return [context]

    return []


# ============================================================
# 8. RUN ONE BIZINSIGHT TEST CASE
# ============================================================

def run_single_test(test: dict):

    test_id = test["id"]
    question = test["question"]
    expected_output = test["expected_output"]

    print()
    print("=" * 90)
    print(f"TEST CASE: {test_id}")
    print("=" * 90)

    print()
    print("Question:")
    print(question)

    # --------------------------------------------------------
    # STEP 1
    # Existing BizInsight RAG Agent
    # --------------------------------------------------------

    try:

        rag_result = rag_agent(
            question
        )

    except Exception as exc:

        print()
        print("RAG AGENT FAILED")
        print(str(exc))

        return None


    if not isinstance(
        rag_result,
        dict
    ):

        print()
        print(
            "RAG AGENT ERROR:"
        )

        print(
            "rag_agent() must return a dictionary."
        )

        return None


    # --------------------------------------------------------
    # STEP 2
    # Extract retrieved context
    # --------------------------------------------------------

    retrieval_context = (
        get_retrieval_context(
            rag_result
        )
    )

    sources = rag_result.get(
        "sources",
        []
    )

    document_count = rag_result.get(
        "document_count",
        0
    )


    print()
    print("RAG Agent Result:")
    print(
        json.dumps(
            rag_result,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )


    print()
    print(
        f"Retrieved Context Count: "
        f"{len(retrieval_context)}"
    )

    print(
        f"Document Count: "
        f"{document_count}"
    )

    print(
        f"Sources: "
        f"{sources}"
    )


    # --------------------------------------------------------
    # STEP 3
    # Existing BizInsight Response Agent
    # --------------------------------------------------------

    try:

        actual_output = response_agent(

            question=question,

            sql_result=None,

            rag_result=rag_result,
        )

    except Exception as exc:

        print()
        print(
            "RESPONSE AGENT FAILED"
        )

        print(
            str(exc)
        )

        actual_output = ""


    if actual_output is None:

        actual_output = ""


    actual_output = str(
        actual_output
    ).strip()


    print()
    print("Expected Answer:")
    print(expected_output)

    print()
    print("Actual Answer:")
    print(actual_output)


    # --------------------------------------------------------
    # STEP 4
    # DeepEval test case
    # --------------------------------------------------------

    test_case = LLMTestCase(

        input=question,

        actual_output=actual_output,

        expected_output=expected_output,

        retrieval_context=retrieval_context,
    )


    return {
        "test_case": test_case,

        "metadata": {
            "id": test_id,
            "question": question,
            "expected_output": expected_output,
            "actual_output": actual_output,
            "retrieval_context": retrieval_context,
            "sources": sources,
            "document_count": document_count,
        },
    }


# ============================================================
# 9. MAIN EVALUATION
# ============================================================

def main():

    print()
    print("=" * 90)
    print("BIZINSIGHT AI - DEEPEVAL RAG EVALUATION")
    print("=" * 90)

    print()
    print(
        f"Evaluation Model: {EVAL_MODEL_NAME}"
    )

    print(
        f"Dataset: {DATASET_PATH}"
    )

    print()
    print(
        "Metrics:"
    )

    print(
        "1. Contextual Relevancy"
    )

    print(
        "2. Contextual Precision"
    )

    print(
        "3. Contextual Recall"
    )

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    dataset = load_test_cases()

    print()
    print(
        f"Dataset Size: {len(dataset)}"
    )

    # --------------------------------------------------------
    # Run BizInsight agents
    # --------------------------------------------------------

    deepeval_test_cases = []
    metadata = []

    for test in dataset:

        result = run_single_test(
            test
        )

        if result is None:

            print()
            print(
                f"Skipping test case: "
                f"{test['id']}"
            )

            continue

        deepeval_test_cases.append(
            result["test_case"]
        )

        metadata.append(
            result["metadata"]
        )


    # --------------------------------------------------------
    # Make sure we have tests
    # --------------------------------------------------------

    if not deepeval_test_cases:

        raise RuntimeError(
            "No valid DeepEval test cases were generated."
        )


    # --------------------------------------------------------
    # Run DeepEval
    # --------------------------------------------------------

    print()
    print("=" * 90)
    print("STARTING DEEPEVAL")
    print("=" * 90)

    results = evaluate(

        test_cases=deepeval_test_cases,

        metrics=METRICS,
    )


    # --------------------------------------------------------
    # Save BizInsight inputs / outputs
    # --------------------------------------------------------

    output_file = (
        RESULTS_DIR
        / "rag_evaluation_cases.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False,
        )


    # --------------------------------------------------------
    # FINAL MESSAGE
    # --------------------------------------------------------

    print()
    print("=" * 90)
    print("DEEPEVAL RAG EVALUATION COMPLETED")
    print("=" * 90)

    print()
    print(
        "Evaluation cases saved to:"
    )

    print(
        output_file
    )

    print()
    print(
        "Metrics evaluated:"
    )

    print(
        "- Contextual Relevancy"
    )

    print(
        "- Contextual Precision"
    )

    print(
        "- Contextual Recall"
    )

    print()
    print(
        "The DeepEval result summary is shown above."
    )


# ============================================================
# 10. ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
