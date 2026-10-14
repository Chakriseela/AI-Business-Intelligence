from backend.Phoenix_evaluation.evaluators.common.judge import (
    evaluate_with_judge
)


GROUNDEDNESS_RUBRIC = """
Evaluate whether the AI response is supported
by the retrieved document context.

Scoring:

100 = Every factual claim is supported by context.
90 = Nearly all claims are supported.
75 = Mostly supported.
50 = Partially supported.
25 = Mostly unsupported.
0 = No meaningful support from context.

Intermediate scores are allowed.

Use the retrieved context as the evidence source.

Do not treat the expected answer as a substitute
for retrieved context.
"""


def groundedness(input, output, expected):

    context = output.get(
        "context",
        ""
    )

    if not context or not str(context).strip():

        return {
            "label": "NOT_EVALUATED",
            "explanation": (
                "Retrieved context is unavailable. "
                "Groundedness requires actual RAG evidence."
            )
        }

    return evaluate_with_judge(
        metric="Groundedness",
        question=input["question"],
        prediction=output["answer"],
        ground_truth=expected["answer"],
        context=str(context),
        rubric=GROUNDEDNESS_RUBRIC
    )
