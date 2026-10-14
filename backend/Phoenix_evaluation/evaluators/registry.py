from backend.Phoenix_evaluation.evaluators.llm_judge.correctness import (
    correctness
)

from backend.Phoenix_evaluation.evaluators.llm_judge.relevance import (
    relevance
)

from backend.Phoenix_evaluation.evaluators.llm_judge.hallucination import (
    hallucination
)

from backend.Phoenix_evaluation.evaluators.llm_judge.groundedness import (
    groundedness
)


def get_evaluators():

    return {
        "correctness": correctness,
        "relevance": relevance,
        "hallucination_safety": hallucination,
        "groundedness": groundedness
    }
