import shutil
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config.settings import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    KNOWLEDGE_BASE_DIR,
    VECTOR_STORE_DIR,
)
from backend.rag.vector_store import get_vector_store


def load_pdfs() -> list:
    pdf_files = sorted(KNOWLEDGE_BASE_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in: {KNOWLEDGE_BASE_DIR}"
        )

    documents = []
    for pdf_path in pdf_files:
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = pdf_path.name
            doc.metadata["file_path"] = str(pdf_path)

        documents.extend(docs)

    return documents


def split_documents(documents: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def reset_vector_store() -> None:
    if VECTOR_STORE_DIR.exists():
        shutil.rmtree(VECTOR_STORE_DIR)


def ingest(reset: bool = True) -> None:
    if reset:
        reset_vector_store()

    documents = load_pdfs()
    chunks = split_documents(documents)
    vector_store = get_vector_store()

    # Explicit IDs make the indexed records traceable and reproducible.
    ids = [f"chunk-{index:05d}" for index in range(len(chunks))]
    vector_store.add_documents(documents=chunks, ids=ids)

    print(f"Knowledge base: {KNOWLEDGE_BASE_DIR}")
    print(f"PDF pages loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Chroma directory: {VECTOR_STORE_DIR}")


if __name__ == "__main__":
    ingest(reset=True)
