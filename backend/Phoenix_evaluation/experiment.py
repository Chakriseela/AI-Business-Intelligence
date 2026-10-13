import pandas as pd

from backend.Phoenix_evaluation.client import ask


def run_experiment(dataset_path):

    df = pd.read_csv(dataset_path)

    results = []

    for _, row in df.iterrows():

        print("=" * 60)

        print("Question:")
        print(row["question"])

        prediction = ask(row["question"])

        print("\nAnswer:")
        print(prediction["answer"])

        results.append(
            {
                "question": row["question"],
                "prediction": prediction["answer"],
                "ground_truth": row["ground_truth"],
                "category": row["category"],
                "latency": prediction["latency"],
            }
        )

        print(results)

    return results
