             RAG
              |
       ┌──────┴──────┐
       ↓             ↓
   Retrieval       Answer
       |             |
 Precision        Faithfulness
 Recall           Relevancy

********************
*  RAGAS Metrics
********************
1. Faithfulness
2. Answer Relevancy
3. Context Precision
        This evaluates whether the retrieved documents contain relevant 
        information, and whether irrelevant information is ranked lower.
        Example:
        Question:
        What is the eligibility criteria?
        Retrieved:
        1. Eligibility criteria       ← relevant
        2. Application procedure      ← somewhat relevant
        3. Payment history             ← irrelevant
        4. Scheme launch date          ← irrelevant
        A good retriever should rank the useful information highly.

4. Context Recall
        Question:
        Did the retrieval system retrieve all the information necessary to answer the question?
        Suppose the correct answer requires:
        Eligibility:
        - Farmer must own agricultural land
        - Must meet income criteria
        - Must have valid documents
        But retrieval only gives:
        Farmer must own agricultural land.
        The retriever missed important information.
        ❌ Low context recall.

Faithfulness
    Is the response supported by the context?
Contextual Relevancy
    Is retrieved context relevant?
Contextual Recall
    Did retrieval capture the required information?
Contextual Precision
    Was relevant context ranked appropriately?


********************
*   DeepEval
********************
DeepEval is another important framework.
It is more general than just traditional RAG evaluation.
You can evaluate:
LLM applications
RAG
Agents
Chatbots
Multi-agent systems


*********************
*   Arize Phoenix
*********************
Phoenix is mainly focused on:
Observability + Evaluation
It can help monitor:
LLM calls
Retrieval
Latency
Token usage
Traces
Embeddings
Hallucination


*********************
*LLM-as-a-Judge
*********************
Architecture:

User Question
      ↓
     LLM
      ↓
Generated Answer
      ↓
   Evaluator LLM
      ↓
 ┌────┴────┐
 ↓         ↓
Score    Reason


***********************************
*   Evaluation Pipeline           *
***********************************
                 Evaluation Dataset
                         ↓
                 ┌───────────────┐
                 │   RAG System  │
                 └───────┬───────┘
                         ↓
               ┌──────────────────┐
               │ Retrieved Context│
               └────────┬─────────┘
                        ↓
                    LLM Answer
                        ↓
              ┌────────────────────┐
              │Evaluation Framework│
              └─────────┬──────────┘
                        ↓
       ┌────────────────┼────────────────┐
       ↓                ↓                ↓
 Retrieval          Generation       Performance
 metrics             metrics           metrics
       ↓                ↓                ↓
 Precision          Faithfulness       Latency
 Recall             Relevancy          Cost



              Evaluation Dataset
                     │
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
   Question                 Ground Truth
        │                  ┌──────────────┐
        │                  │ Expected     │
        │                  │ Answer       │
        │                  │ Relevant Docs│
        │                  └──────────────┘
        ↓
     RAG System
        │
        ├──────────────→ Retrieved Documents
        │                       │
        ↓                       ↓
    LLM Answer          Retrieval Evaluation
        │                       │
        │                       ├── Precision
        │                       └── Recall
        ↓
 Generation Evaluation
        │
        ├── Faithfulness
        └── Answer Relevancy




1. Retrieval / Evaluation Metrics
These evaluate whether your retriever/vector DB found the right chunks.

| Metric                | What it checks                                                                   |
| --------------------- | -------------------------------------------------------------------------------- |
| **Precision@K**       | Of the top K retrieved chunks, how many are relevant?                            |
| **Recall@K**          | Of all relevant chunks, how many did we retrieve?                                |
| **Hit Rate@K**        | Did at least one correct/relevant chunk appear in top K?                         |
| **MRR**               | How high was the first relevant chunk ranked?                                    |
| **NDCG@K**            | How good is the overall ranking of retrieved chunks?                             |
| **Context Precision** | Are relevant contexts ranked ahead of irrelevant ones?                           |
| **Context Recall**    | Did retrieved context contain enough information needed for the expected answer? |
| **Context Relevancy** | How relevant is retrieved context to the user's question?                        |


2. Generation Metrics
These evaluate the answer produced by the LLM after retrieval.

| Metric                          | What it checks                                                        |
| ------------------------------- | --------------------------------------------------------------------- |
| **Faithfulness / Groundedness** | Is the answer supported by retrieved context?                         |
| **Answer Relevancy**            | Does the answer actually address the question?                        |
| **Answer Correctness**          | Is the answer correct compared with the expected/reference answer?    |
| **Semantic Similarity**         | Is the generated answer semantically similar to the reference answer? |
| **Exact Match**                 | Does generated output exactly match the expected answer?              |
| **ROUGE**                       | Measures text overlap, commonly for generated text                    |
| **BLEU**                        | Measures n-gram overlap with reference text                           |
| **BERTScore**                   | Measures semantic similarity using contextual embeddings              |
| **Hallucination**               | Does the answer contain unsupported/generated claims?                 |



**If retrieval is wrong, investigate:**
    Embedding model
    Chunk size
    Chunk overlap
    Top K
    Metadata filtering
    Query rewriting
    Reranking

**If retrieval is correct but generation is wrong, investigate:**
    Prompt
    Context formatting
    LLM
    Faithfulness
    Temperature
    Context window



"How would you implement RAG evaluation in a real project?"
You can answer:
    "I would evaluate the RAG pipeline at two levels:
    retrieval and generation. For retrieval, I would create a golden dataset and
    measure metrics such as Precision@K, Recall@K, MRR, Context Precision and Context Recall.
    For generation, I would evaluate Faithfulness, Answer Relevancy and Answer Correctness.
    I would run these evaluations offline whenever I change chunking, embeddings, Top-K, reranking, prompts or models.
    For production, I would add tracing and monitoring using a tool such as
    Phoenix or LangSmith and combine automated evaluation with human feedback."




****************************************
#       Final cheat sheet              *
****************************************

                 RAG EVALUATION
                       │
          ┌────────────┴────────────┐
          │                         │
      RETRIEVAL                 GENERATION
          │                         │
     Precision@K                Faithfulness 
     Recall@K                   Answer Relevancy
     Hit Rate                   Answer Correctness
     MRR                        Semantic Similarity
     NDCG                       Hallucination
     Context Precision
     Context Recall
     Context Relevancy


Frameworks
────────────────
Ragas       → RAG evaluation
DeepEval    → LLM testing
Phoenix     → Tracing + evaluation
LangSmith   → LangChain tracing/evaluation
TruLens     → RAG evaluation/observability


Debugging
────────────────
Wrong answer
     ↓
Check retrieved context
     ↓
Wrong context? → Fix retrieval
Right context? → Fix generation