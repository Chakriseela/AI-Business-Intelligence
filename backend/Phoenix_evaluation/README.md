
                BIZINSIGHT AI
                       |
                       |
              Phoenix Evaluation
                       |
                       v
              bizinsight_dataset.csv
                       |
                       v
                 Phoenix Client
                       |
                       v
               Register Dataset
                       |
                       v
                Run Experiment
                       |
                       v
                 client.ask()
                       |
                       v
              BizInsight Workflow
                       |
              +--------+--------+
              |                 |
              v                 v
          SQL Agent         RAG Agent
              |                 |
              +--------+--------+
                       |
                       v
                Response Agent
                       |
                       v
                  Prediction
                       |
                       v
                 LLM Evaluators
                       |
             +---------+---------+
             |         |         |
             v         v         v
        Correctness Relevance Unsupported
                                Claims
             |         |         |
             +---------+---------+
                       |
                       v
              Phoenix Experiments
                       |
                       v
                Phoenix Dashboard