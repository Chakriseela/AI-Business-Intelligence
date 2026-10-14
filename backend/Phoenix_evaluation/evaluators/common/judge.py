import json

from google import genai
from google.genai import types

from backend.Phoenix_evaluation.config import (
    GEMINI_API_KEY,
    JUDGE_MODEL
)


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY or GOOGLE_API_KEY is missing."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def evaluate_with_judge(
    metric: str,
    question: str,
    prediction: str,
    ground_truth: str,
    rubric: str,
    context: str = ""
):

    prompt = f"""
You are an expert evaluator for an enterprise
business intelligence AI assistant.

Evaluate the response using the specified rubric.

METRIC:
{metric}

QUESTION:
{question}

AI RESPONSE:
{prediction}

GROUND TRUTH:
{ground_truth}

RETRIEVED CONTEXT:
{context}

EVALUATION RUBRIC:
{rubric}

Instructions:

1. Evaluate only the requested metric.
2. Follow the supplied rubric.
3. Assign a score between 0 and 100.
4. Provide a concise explanation.
5. Do not assume unsupported facts are true.
6. Treat the provided reference as authoritative
   for the facts it explicitly states.
7. Ignore harmless formatting differences.

Return JSON only:

{{
    "score": 85,
    "reason": "Explanation for the score"
}}
"""

    response = client.models.generate_content(
        model=JUDGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json"
        )
    )

    if not response.text:
        raise ValueError(
            "Judge returned an empty response."
        )

    result = json.loads(response.text)

    score = float(result["score"])

    if not 0 <= score <= 100:
        raise ValueError(
            f"Invalid judge score: {score}"
        )

    reason = str(
        result.get("reason", "")
    )

    return {
        "score": score,
        "label": (
            "PASS"
            if score >= 85
            else "FAIL"
        ),
        "explanation": reason
    }
