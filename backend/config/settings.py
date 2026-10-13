from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:0.8b")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"
VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store" / "chroma_db"
COLLECTION_NAME = "bizinsight_knowledge"
EMBEDDING_MODEL = "models/gemini-embedding-001"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
TOP_K = 4


#=========================================================
# Phoenix 
#=========================================================
PHOENIX_PROJECT_NAME = "bizinsight-ai"
PHOENIX_ENDPOINT = "http://localhost:6006"

#=========================================================
# Dataset
#=========================================================
DATASET_PATH = PROJECT_ROOT / "backend" / "Phoenix_evaluation" / "datasets" / "bizinsight_dataset.csv"
PHOENIX_DATASET_NAME = "bizinsight-evaluation-dataset"
EVALUATION_JUDGE_MODEL = "gemini-2.5-flash"

#=========================================================
# EXPERIMENT CONFIGURATION
#=========================================================
EXPERIMENT_NAME = "BizInsight-RAG-Evaluation-Experiment"

EXPERIMENT_DESCRIPTION = (
    "Evaluation of BizInsight AI using "
    "correctness, relevance and "
    "unsupported-claims metrics. "
)