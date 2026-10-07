# BizInsight - DeepEval Evaluation

## Stage 1: RAG Retrieval Evaluation

This stage evaluates the existing BizInsight retriever with:

- Contextual Relevancy
- Contextual Precision
- Contextual Recall

The evaluation does not replace the existing RAG pipeline. It imports the current `retrieve_context()` function and converts its output into DeepEval `LLMTestCase` objects.

## Setup

From the BizInsight project root:

```bash
pip install -U -r DeepEval_evaluation/requirements.txt
```

Set a Gemini key in the project's `.env`:

```env
GEMINI_API_KEY=your_key
```

The evaluator maps this to `GOOGLE_API_KEY` for DeepEval.

If your retriever is not at `backend.rag.retriever:retrieve_context`, set:

```env
RAG_RETRIEVER_IMPORT=your.module.path:retrieve_context
```

Optionally set:

```env
DEEPEVAL_MODEL=gemini-2.5-flash
```

## Dataset

Edit:

`DeepEval_evaluation/datasets/rag_test_cases.csv`

Each row needs:

- `id`
- `question`
- `expected_output`

Expected output should be the trusted/reference answer for that question.

## Run

From the BizInsight project root:

```bash
python DeepEval_evaluation/rag_evaluation/run_rag_evaluation.py
```

## Important

For the best retriever evaluation, the existing retriever should ideally expose the retrieved chunks as a list rather than only one concatenated context string. The adapter supports both, but list[str] preserves the real retrieval boundaries and ranking order better.
