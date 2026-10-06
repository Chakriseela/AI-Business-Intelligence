# BizInsight AI - RAG Layer

## What this does

PDF files in `knowledge_base/` are loaded, split into overlapping text chunks, embedded with Gemini, and persisted in ChromaDB under `vector_store/chroma_db/`.

The retriever then turns a user question into an embedding and performs semantic similarity search over those stored chunks.

## Files
- `backend/rag/ingest.py` - PDF loading, chunking, and indexing.
- `backend/rag/vector_store.py` - Gemini embeddings + persistent Chroma connection.
- `backend/rag/retriever.py` - semantic retrieval and a simple test CLI.
- `backend/config/settings.py` - project paths and RAG settings.

## Setup

From the project root:

```powershell
pip install -r requirements_rag.txt
```

Create `.env` and add:

```text
GEMINI_API_KEY=your_actual_key
```

Put the PDF files in:

```text
knowledge_base/
```

## Build the vector database

```powershell
python -m backend.rag.ingest
```

## Test retrieval

```powershell
python -m backend.rag.retriever
```

Try:

```text
What is the Platinum discount?
```

The console should show the most relevant chunks and the source PDF/page metadata.

```
pip install arize-phoenix openinference-instrumentation openinference-instrumentation-langchain



python -m backend.rag.ingest
python -m backend.rag.retriever
python -m backend.mcp_server.server
python -m backend.mcp_server.client
python -m backend.agents.sql_agent
python -m backend.agents.orchestrator
python -m backend.main
```

# Evaluations
```
python -m backend.evaluation.run_evaluation
python -m backend.evaluation.ragas_evaluation


cd frontend-react
npm install @xyflow/react
npm install @xyflow/react lucide-react react-markdown
```

The App.jsx uses the existing ws://127.0.0.1:8000/ws/chat endpoint and sends question, model_provider, and model_name.




# TO RUN THE APPLICATION
```
python -m backend.main  (in root dir)
cd frontend-react
npm run dev
phoenix serve
python -m backend.evaluation.run_evaluation
```