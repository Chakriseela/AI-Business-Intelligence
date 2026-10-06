# import os
# from functools import lru_cache

# import ollama
# from dotenv import load_dotenv
# from langchain_chroma import Chroma
# from langchain_core.embeddings import Embeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# from backend.config.settings import (
#     COLLECTION_NAME,
#     EMBEDDING_MODEL,
#     VECTOR_STORE_DIR,
# )

# load_dotenv()


# # =========================================================
# # Gemini API Key
# # =========================================================

# def _get_api_key() -> str:
#     api_key = os.getenv("GEMINI_API_KEY")

#     if not api_key:
#         raise RuntimeError(
#             "GEMINI_API_KEY is not set in .env"
#         )

#     return api_key


# # =========================================================
# # Ollama Embedding Wrapper
# # =========================================================

# class OllamaQwenEmbeddings(Embeddings):
#     """
#     LangChain-compatible wrapper around the ollama package.
#     """

#     def __init__(
#         self,
#         model: str = "qwen3-embedding:4b",
#     ):
#         self.model = model

#     def embed_documents(
#         self,
#         texts: list[str],
#     ) -> list[list[float]]:

#         response = ollama.embed(
#             model=self.model,
#             input=texts,
#         )

#         return response["embeddings"]

#     def embed_query(
#         self,
#         text: str,
#     ) -> list[float]:

#         response = ollama.embed(
#             model=self.model,
#             input=text,
#         )

#         return response["embeddings"][0]


# # =========================================================
# # Gemini Embeddings
# # =========================================================

# @lru_cache(maxsize=1)
# def get_gemini_embeddings():

#     api_key = _get_api_key()

#     return GoogleGenerativeAIEmbeddings(
#         model=EMBEDDING_MODEL,
#         google_api_key=api_key,
#     )


# # =========================================================
# # Ollama Embeddings
# # =========================================================

# @lru_cache(maxsize=1)
# def get_ollama_embeddings():

#     return OllamaQwenEmbeddings(
#         model="qwen3-embedding:4b"
#     )


# # =========================================================
# # Select Embedding Provider
# # =========================================================

# def get_embeddings():

#     try:

#         print(
#             "Trying Gemini embeddings..."
#         )

#         embeddings = get_gemini_embeddings()

#         # Test actual API call
#         embeddings.embed_query(
#             "BizInsight embedding test"
#         )

#         print(
#             "Using Gemini embeddings."
#         )

#         return embeddings, "gemini"

#     except Exception as gemini_error:

#         print(
#             f"Gemini embedding failed: {gemini_error}"
#         )

#         print(
#             "Falling back to Ollama "
#             "qwen3-embedding:4b..."
#         )

#         embeddings = get_ollama_embeddings()

#         # Test Ollama
#         embeddings.embed_query(
#             "BizInsight embedding test"
#         )

#         print(
#             "Using Ollama embeddings."
#         )

#         return embeddings, "ollama"


# # =========================================================
# # Get Chroma Vector Store
# # =========================================================

# def get_vector_store():

#     embeddings, provider = get_embeddings()

#     # Keep Gemini and Ollama vector spaces separate
#     provider_dir = (
#         VECTOR_STORE_DIR / provider
#     )

#     provider_dir.mkdir(
#         parents=True,
#         exist_ok=True
#     )

#     collection_name = (
#         f"{COLLECTION_NAME}_{provider}"
#     )

#     return Chroma(
#         collection_name=collection_name,
#         embedding_function=embeddings,
#         persist_directory=str(
#             provider_dir
#         ),
#     )


# # =========================================================
# # Test
# # =========================================================

# if __name__ == "__main__":

#     embeddings, provider = get_embeddings()

#     print(
#         f"\nEmbedding provider: {provider}"
#     )

#     test_embedding = embeddings.embed_query(
#         "What is the Platinum membership discount?"
#     )

#     print(
#         f"Embedding dimensions: "
#         f"{len(test_embedding)}"
#     )

#     vector_store = get_vector_store()

#     print(
#         "\nChroma vector store initialized successfully."
#     )




































import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.config.settings import COLLECTION_NAME, EMBEDDING_MODEL, VECTOR_STORE_DIR

load_dotenv()


def _get_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your .env file before running the RAG pipeline."
        )
    return api_key


@lru_cache(maxsize=1)
def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    api_key = _get_api_key()
    os.environ.setdefault("GOOGLE_API_KEY", api_key)

    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
    )


def get_vector_store() -> Chroma:
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(VECTOR_STORE_DIR),
    )
