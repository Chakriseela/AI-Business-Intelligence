import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT_DIR.parent

# Load the BizInsight project's .env first, then this folder's .env if present.
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(ROOT_DIR / ".env", override=False)

# DeepEval's Gemini integration uses GOOGLE_API_KEY.
# This lets your existing GEMINI_API_KEY continue to work.
if not os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

os.environ.setdefault("USE_GEMINI_MODEL", "1")

# Use the same Gemini family you already use in BizInsight, or change this one line.
EVAL_MODEL = os.getenv("DEEPEVAL_MODEL", "gemini-2.5-flash")

# IMPORTANT: point this to the module that exposes your existing retrieve_context().
# Examples:
# backend.rag.retriever:retrieve_context
# backend.rag.pipeline:retrieve_context
RAG_RETRIEVER_IMPORT = os.getenv(
    "RAG_RETRIEVER_IMPORT",
    "backend.rag.retriever:retrieve_context",
)

DATASET_FILE = ROOT_DIR / "datasets" / "rag_test_cases.csv"
RESULTS_DIR = ROOT_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
