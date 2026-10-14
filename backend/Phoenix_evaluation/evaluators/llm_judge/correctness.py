from backend.Phoenix_evaluation.evaluators.common.judge import (
    evaluate_with_judge
)


CORRECTNESS_RUBRIC = """
Evaluate factual correctness against the ground truth.

Scoring:

100 = Completely correct and factually consistent.
90 = Correct with negligible omissions.
75 = Mostly correct with minor missing information.
50 = Partially correct.
25 = Mostly incorrect.
0 = Completely incorrect.

Intermediate scores are allowed.

Do not penalize differences in wording.
Penalize factual contradictions.
"""


def correctness(input, output, expected):

    return evaluate_with_judge(
        metric="Correctness",
        question=input["question"],
        prediction=output["answer"],
        ground_truth=expected["answer"],
        rubric=CORRECTNESS_RUBRIC
    )
