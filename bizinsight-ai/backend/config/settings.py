from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.6-flash"
OLLAMA_MODEL = "qwen3.5:0.8b"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"
VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store" / "chroma_db"
COLLECTION_NAME = "bizinsight_knowledge"
EMBEDDING_MODEL = "models/gemini-embedding-001"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
TOP_K = 4
