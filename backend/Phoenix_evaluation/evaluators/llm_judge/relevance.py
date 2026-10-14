from backend.Phoenix_evaluation.evaluators.common.judge import (
    evaluate_with_judge
)


RELEVANCE_RUBRIC = """
Evaluate whether the response directly answers
the user's question.

Scoring:

100 = Fully relevant and directly answers the question.
90 = Highly relevant with minor unnecessary details.
75 = Mostly relevant.
50 = Partially relevant.
25 = Barely relevant.
0 = Completely irrelevant.

Intermediate scores are allowed.

Focus on relevance, not factual correctness.
"""


def relevance(input, output, expected):

    return evaluate_with_judge(
        metric="Relevance",
        question=input["question"],
        prediction=output["answer"],
        ground_truth=expected["answer"],
        rubric=RELEVANCE_RUBRIC
    )
