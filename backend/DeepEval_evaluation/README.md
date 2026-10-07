pip install -U deepeval python-dotenv google-genai




# Phoenix
Collects:
- Traces
- Span hierarchy
- Latency
- Token usage
- Errors
- Agent execution flow

# DeepEval
Evaluates:
- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall
- Hallucination
- Tool Correctness
- Task Completion
- Custom business metrics

```
| Feature | Phoenix | DeepEval |
|---------|----------|-----------|
| Open Source                   | ✅ | ✅ |
| Local Dashboard               | ✅ | ❌ |
| Localhost UI                  | ✅ | ❌ |
| Trace Visualization           | ✅ | Basic locally / Full via Confident AI |
| Evaluation Metrics            | Limited | Excellent |
| RAG Evaluation                | Limited | Excellent |
| Agent Evaluation              | Basic | Excellent |
| Unit Testing                  | ❌ | ✅ |
| PyTest Integration            | ❌ | ✅ |
| CI/CD                         | ❌ | ✅ |
| Observability                 | Excellent | Basic locally |
| Latency Tracking              | Excellent | Available through tracing |
| Token Tracking                | Excellent | Available through tracing |
```

bizinsight-ai/
│
├── backend/
│   ├── agents/
│   ├── rag/
│   ├── mcp_server/
│   └── ...
│
├── DeepEval_evaluation/
│   ├── rag_evaluation/
│   ├── generation_evaluation/
│   ├── agent_evaluation/
│   ├── mcp_evaluation/
│   ├── sql_evaluation/
│   ├── end_to_end/
│   ├── datasets/
│   ├── results/
│   ├── config.py
│   └── README.md



DeepEval_evaluation
        │
        ├── 1. RAG Evaluation
        │      ├── Context Precision
        │      ├── Context Recall
        │      ├── Context Relevancy
        │      └── Faithfulness
        │
        ├── 2. Generation / LLM Evaluation
        │      ├── Answer Relevancy
        │      ├── Correctness
        │      ├── Faithfulness
        │      └── Hallucination
        │
        ├── 3. Agent Evaluation
        │      ├── Task Completion
        │      ├── Agent Trajectory
        │      └── Tool Correctness
        │
        ├── 4. MCP Evaluation
        │      ├── Tool Selection
        │      ├── Tool Arguments
        │      └── Tool Output
        │
        ├── 5. SQL Evaluation
        │      ├── SQL Correctness
        │      ├── Query Result Correctness
        │      └── Answer Correctness
        │
        └── 6. End-to-End Evaluation
               ├── Overall Correctness
               ├── Relevancy
               └── Task Success



