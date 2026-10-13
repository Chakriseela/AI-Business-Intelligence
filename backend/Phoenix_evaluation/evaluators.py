import json
import threading

from functools import lru_cache

from google import genai
from google.genai import types

from backend.config.settings import (
    GEMINI_API_KEY,
    JUDGE_MODEL,
)


# ==========================================
# GEMINI JUDGE CLIENT
# ==========================================

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY or GOOGLE_API_KEY is required."
    )


judge_client = genai.Client(
    api_key=GEMINI_API_KEY
)

judge_lock = threading.Lock()


# ==========================================
# LLM JUDGE PROMPT
# ==========================================

JUDGE_PROMPT = """
You are an expert evaluator for a business
intelligence AI assistant.

Evaluate the AI-generated answer using:

1. User Question
2. Ground Truth
3. AI Prediction

Evaluate three metrics.

------------------------------------------
METRIC 1: CORRECTNESS
------------------------------------------

Determine whether the prediction is factually
consistent with the ground truth.

Scoring:

1.0 = Fully correct
0.75 = Mostly correct
0.5 = Partially correct
0.25 = Mostly incorrect
0.0 = Incorrect

------------------------------------------
METRIC 2: RELEVANCE
------------------------------------------

Determine whether the prediction directly
addresses the user's question.

Scoring:

1.0 = Fully relevant
0.75 = Mostly relevant
0.5 = Partially relevant
0.25 = Mostly irrelevant
0.0 = Irrelevant

------------------------------------------
METRIC 3: UNSUPPORTED CLAIMS
------------------------------------------

Determine whether the prediction introduces
factual claims that are not supported by
the ground truth.

Scoring:

0.0 = No unsupported claims
0.25 = Minor unsupported details
0.5 = Some unsupported claims
0.75 = Several unsupported claims
1.0 = Predominantly unsupported claims

Important:

The ground truth is the reference answer.

Do not assume the reference contains every
possible fact about the world.

If the reference is insufficient to determine
whether an additional claim is true, describe
that uncertainty in the explanation.

Do not penalize harmless formatting differences.

Do not reward answers that contradict
the reference.

------------------------------------------
QUESTION
------------------------------------------

{question}

------------------------------------------
GROUND TRUTH
------------------------------------------

{ground_truth}

------------------------------------------
PREDICTION
------------------------------------------

{prediction}

------------------------------------------
OUTPUT FORMAT
------------------------------------------

Return only valid JSON.

{{
    "correctness": {{
        "score": 0.0,
        "explanation": "Reason"
    }},
    "relevance": {{
        "score": 0.0,
        "explanation": "Reason"
    }},
    "unsupported_claims": {{
        "score": 0.0,
        "explanation": "Reason"
    }}
}}
"""


# ==========================================
# SCORE VALIDATION
# ==========================================

def validate_score(value):

    score = float(value)

    if not 0.0 <= score <= 1.0:
        raise ValueError(
            f"Invalid evaluation score: {score}"
        )

    return score


# ==========================================
# SHARED LLM EVALUATION
# ==========================================

@lru_cache(maxsize=1024)
def evaluate_with_llm(
    question: str,
    prediction: str,
    ground_truth: str
) -> dict:

    prompt = JUDGE_PROMPT.format(
        question=question,
        prediction=prediction,
        ground_truth=ground_truth
    )

    # Serialize judge calls for a predictable
    # local experiment and avoid simultaneous
    # duplicate evaluations.

    with judge_lock:

        response = judge_client.models.generate_content(
            model=JUDGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json"
            )
        )

    if not response.text:
        raise ValueError(
            "Gemini judge returned an empty response."
        )

    result = json.loads(
        response.text
    )

    required_metrics = [
        "correctness",
        "relevance",
        "unsupported_claims"
    ]

    for metric in required_metrics:

        if metric not in result:
            raise ValueError(
                f"Missing metric: {metric}"
            )

        result[metric]["score"] = validate_score(
            result[metric]["score"]
        )

    return result


# ==========================================
# CORRECTNESS EVALUATOR
# ==========================================

def correctness(
    input,
    output,
    expected
):

    result = evaluate_with_llm(
        question=input["question"],
        prediction=output["answer"],
        ground_truth=expected["answer"]
    )

    metric = result["correctness"]

    return {
        "score": metric["score"],
        "label": "correctness",
        "explanation": metric["explanation"]
    }


# ==========================================
# RELEVANCE EVALUATOR
# ==========================================

def relevance(
    input,
    output,
    expected
):

    result = evaluate_with_llm(
        question=input["question"],
        prediction=output["answer"],
        ground_truth=expected["answer"]
    )

    metric = result["relevance"]

    return {
        "score": metric["score"],
        "label": "relevance",
        "explanation": metric["explanation"]
    }


# ==========================================
# UNSUPPORTED CLAIMS EVALUATOR
# ==========================================

def unsupported_claims(
    input,
    output,
    expected
):

    result = evaluate_with_llm(
        question=input["question"],
        prediction=output["answer"],
        ground_truth=expected["answer"]
    )

    metric = result["unsupported_claims"]

    return {
        "score": metric["score"],
        "label": "unsupported_claims",
        "explanation": metric["explanation"]
    }


# ==========================================
# REGISTER EVALUATORS
# ==========================================

def get_evaluators():

    return {
        "correctness": correctness,
        "relevance": relevance,
        "unsupported_claims": unsupported_claims
    }
