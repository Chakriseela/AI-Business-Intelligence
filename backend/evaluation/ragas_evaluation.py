import asyncio
import os

from dotenv import load_dotenv

from ragas import SingleTurnSample
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    LLMContextRecall,
    LLMContextPrecisionWithoutReference,
)

from backend.agents.rag_agent import rag_agent
from backend.agents.response_agent import response_agent


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")


# ============================================================
# 2. TEST DATASET
# ============================================================

TEST_CASES = [
    {
        "id": "RET-001",
        "question": "What is the return window for electronics?",
        "reference": "Electronics can be returned within 30 days of purchase.",
    },
    {
        "id": "RET-002",
        "question": "Can opened software be returned?",
        "reference": "Opened software cannot be returned.",
    },
    {
        "id": "RET-003",
        "question": "Who pays the return shipping cost?",
        "reference": "The customer is responsible for return shipping costs.",
    },
]


# ============================================================
# 3. RUN ONE TEST CASE
# ============================================================

async def evaluate_one(test_case: dict):

    question = test_case["question"]
    reference = test_case["reference"]

    print("\n" + "=" * 80)
    print(f"TEST CASE: {test_case['id']}")
    print("=" * 80)

    print(f"\nQuestion:\n{question}")

    # --------------------------------------------------------
    # STEP A: RUN YOUR EXISTING RAG AGENT
    # --------------------------------------------------------

    rag_result = rag_agent(question)

    context = rag_result.get("context", "")
    sources = rag_result.get("sources", [])

    print("\nRetrieved Context:")
    print(context)

    print("\nSources:")
    print(sources)

    # --------------------------------------------------------
    # STEP B: CONVERT CONTEXT INTO LIST OF CHUNKS
    # --------------------------------------------------------

    retrieved_contexts = [
        chunk.strip()
        for chunk in context.split("\n\n")
        if chunk.strip()
    ]

    if not retrieved_contexts:
        print("\nNo context retrieved.")
        return

    # --------------------------------------------------------
    # STEP C: RUN YOUR RESPONSE AGENT
    # --------------------------------------------------------

    # Adjust this call according to your existing
    # response_agent.py signature.
    try:
        response_result = response_agent(
            question=question,
            context=context
        )

        # Handle dictionary response
        if isinstance(response_result, dict):
            answer = response_result.get(
                "answer",
                response_result.get(
                    "final_answer",
                    str(response_result)
                )
            )
        else:
            answer = str(response_result)

    except Exception as exc:
        print(f"\nResponse agent error: {exc}")
        answer = ""

    print("\nGenerated Answer:")
    print(answer)

    # --------------------------------------------------------
    # STEP D: CREATE RAGAS SAMPLE
    # --------------------------------------------------------

    sample = SingleTurnSample(
        user_input=question,
        retrieved_contexts=retrieved_contexts,
        response=answer,
        reference=reference,
    )

    # --------------------------------------------------------
    # STEP E: CREATE METRICS
    # --------------------------------------------------------

    faithfulness = Faithfulness()

    answer_relevancy = AnswerRelevancy()

    context_recall = LLMContextRecall()

    context_precision = LLMContextPrecisionWithoutReference()

    # --------------------------------------------------------
    # STEP F: EVALUATE
    # --------------------------------------------------------

    results = {}

    try:
        results["faithfulness"] = (
            await faithfulness.single_turn_ascore(sample)
        )
    except Exception as exc:
        print(f"Faithfulness error: {exc}")
        results["faithfulness"] = None

    try:
        results["answer_relevancy"] = (
            await answer_relevancy.single_turn_ascore(sample)
        )
    except Exception as exc:
        print(f"Answer relevancy error: {exc}")
        results["answer_relevancy"] = None

    try:
        results["context_recall"] = (
            await context_recall.single_turn_ascore(sample)
        )
    except Exception as exc:
        print(f"Context recall error: {exc}")
        results["context_recall"] = None

    try:
        results["context_precision"] = (
            await context_precision.single_turn_ascore(sample)
        )
    except Exception as exc:
        print(f"Context precision error: {exc}")
        results["context_precision"] = None

    # --------------------------------------------------------
    # STEP G: PRINT RESULTS
    # --------------------------------------------------------

    print("\n" + "-" * 80)
    print("RAGAS SCORES")
    print("-" * 80)

    for metric, score in results.items():

        if score is None:
            print(f"{metric}: ERROR")
        else:
            print(f"{metric}: {score:.4f}")

    return {
        "id": test_case["id"],
        "question": question,
        "reference": reference,
        "answer": answer,
        "contexts": retrieved_contexts,
        "sources": sources,
        "scores": results,
    }


# ============================================================
# 4. RUN ALL TEST CASES
# ============================================================

async def main():

    print("\n")
    print("=" * 80)
    print("STARTING RAGAS EVALUATION")
    print("=" * 80)

    all_results = []

    for test_case in TEST_CASES:

        try:
            result = await evaluate_one(test_case)

            if result:
                all_results.append(result)

        except Exception as exc:
            print(
                f"\nTest case {test_case['id']} failed: {exc}"
            )

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print("\n\n")
    print("=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)

    metric_names = [
        "faithfulness",
        "answer_relevancy",
        "context_recall",
        "context_precision",
    ]

    for metric in metric_names:

        scores = [
            result["scores"][metric]
            for result in all_results
            if result["scores"].get(metric) is not None
        ]

        if scores:
            average = sum(scores) / len(scores)
            print(
                f"{metric:25} : {average:.4f}"
            )
        else:
            print(
                f"{metric:25} : No result"
            )


# ============================================================
# 5. ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())