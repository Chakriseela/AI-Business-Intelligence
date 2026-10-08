import os
import csv
import json
from pathlib import Path

from dotenv import load_dotenv

from deepeval import evaluate
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
)
from deepeval.test_case import LLMTestCase

from backend.agents import rag_agent
from backend.agents import response_agent


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# Your existing application may use GEMINI_API_KEY.
# DeepEval's Gemini integration expects GOOGLE_API_KEY.
if not os.getenv("GOOGLE_API_KEY"):
    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_key:
        os.environ["GOOGLE_API_KEY"] = gemini_key


# Tell DeepEval to use Gemini
os.environ["USE_GEMINI_MODEL"] = "1"

# Use the model you want for evaluation.
# You can change this through the environment if required.
EVAL_MODEL = os.getenv(
    "DEEPEVAL_MODEL",
    "gemini-3.6-flash"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    BASE_DIR
    / "datasets"
    / "rag_test_cases.csv"
)

RESULTS_DIR = (
    BASE_DIR
    / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_test_cases():

    test_cases = []

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            test_cases.append({
                "id": row["id"].strip(),
                "question": row["question"].strip(),
                "expected_output": row[
                    "expected_output"
                ].strip(),
            })

    return test_cases


# ============================================================
# CONVERT RETRIEVAL RESULT
# ============================================================

def build_retrieval_context(
    rag_result: dict
) -> list[str]:

    context = rag_result.get(
        "context",
        ""
    )

    # Your current rag_agent returns
    # context as one string.
    #
    # DeepEval expects:
    #
    # retrieval_context=[
    #     "chunk 1",
    #     "chunk 2",
    #     ...
    # ]

    if isinstance(context, list):

        return [
            str(chunk).strip()
            for chunk in context
            if str(chunk).strip()
        ]

    if isinstance(context, str):

        context = context.strip()

        if context:
            return [context]

    return []


# ============================================================
# CREATE DEEPEVAL METRICS
# ============================================================

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


# ============================================================
# MAIN EVALUATION
# ============================================================

def run_evaluation():

    print()
    print("=" * 80)
    print("BIZINSIGHT AI - DEEPEVAL RAG EVALUATION")
    print("=" * 80)

    print(
        f"Evaluation model: {EVAL_MODEL}"
    )

    dataset = load_test_cases()

    print(
        f"Dataset size: {len(dataset)}"
    )

    print("=" * 80)


    deepeval_test_cases = []

    evaluation_metadata = []


    # --------------------------------------------------------
    # RUN BIZINSIGHT RAG FOR EACH QUESTION
    # --------------------------------------------------------

    for test in dataset:

        test_id = test["id"]
        question = test["question"]
        expected_output = test[
            "expected_output"
        ]


        print()
        print("=" * 80)
        print(f"TEST CASE: {test_id}")
        print("=" * 80)

        print()
        print("Question:")
        print(question)


        # ----------------------------------------------------
        # 1. RUN YOUR EXISTING RAG AGENT
        # ----------------------------------------------------

        try:

            rag_result = rag_agent(
                question
            )

        except Exception as exc:

            print()
            print(
                f"RAG AGENT ERROR: {exc}"
            )

            continue


        # ----------------------------------------------------
        # 2. EXTRACT RETRIEVED CONTEXT
        # ----------------------------------------------------

        retrieval_context = (
            build_retrieval_context(
                rag_result
            )
        )


        print()
        print(
            "Retrieved context count:"
        )

        print(
            len(retrieval_context)
        )


        if not retrieval_context:

            print(
                "WARNING: No retrieval context found."
            )


        # ----------------------------------------------------
        # 3. RUN YOUR EXISTING RESPONSE AGENT
        # ----------------------------------------------------

        try:

            actual_output = response_agent(
                question=question,
                sql_result=None,
                rag_result=rag_result,
            )

        except Exception as exc:

            print()
            print(
                f"RESPONSE AGENT ERROR: {exc}"
            )

            actual_output = ""


        # Make sure output is always string
        if actual_output is None:

            actual_output = ""

        actual_output = str(
            actual_output
        )


        print()
        print("Generated Answer:")
        print(actual_output)


        # ----------------------------------------------------
        # 4. CREATE DEEPEVAL TEST CASE
        # ----------------------------------------------------

        deepeval_case = LLMTestCase(

            input=question,

            actual_output=actual_output,

            expected_output=expected_output,

            retrieval_context=retrieval_context,
        )


        deepeval_test_cases.append(
            deepeval_case
        )


        evaluation_metadata.append({

            "id": test_id,

            "question": question,

            "expected_output":
                expected_output,

            "actual_output":
                actual_output,

            "retrieval_context":
                retrieval_context,

            "sources":
                rag_result.get(
                    "sources",
                    []
                ),

            "document_count":
                rag_result.get(
                    "document_count",
                    0
                ),
        })


    # --------------------------------------------------------
    # RUN DEEPEVAL
    # --------------------------------------------------------

    if not deepeval_test_cases:

        print()
        print(
            "No test cases were created."
        )

        return


    print()
    print("=" * 80)
    print("STARTING DEEPEVAL METRICS")
    print("=" * 80)


    results = evaluate(

        test_cases=deepeval_test_cases,

        metrics=metrics,
    )


    # --------------------------------------------------------
    # SAVE RAW INFORMATION
    # --------------------------------------------------------

    output_file = (
        RESULTS_DIR
        / "rag_evaluation_cases.json"
    )


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            evaluation_metadata,
            file,
            indent=4,
            ensure_ascii=False,
        )


    print()
    print("=" * 80)
    print("RAG EVALUATION COMPLETED")
    print("=" * 80)

    print()
    print(
        f"Evaluation data saved to:"
    )

    print(
        output_file
    )

    print()


if __name__ == "__main__":

    run_evaluation()
