import hashlib

import pandas as pd

from phoenix.client import Client

from backend.Phoenix_evaluation.client import ask

from backend.Phoenix_evaluation.evaluators import (
    get_evaluators
)

from backend.Phoenix_evaluation.config import (
    PHOENIX_BASE_URL,
    PHOENIX_API_KEY,
    PHOENIX_DATASET_NAME,
    DATASET_PATH,
    EXPERIMENT_NAME,
    EXPERIMENT_DESCRIPTION,
    JUDGE_MODEL,
)


# ==========================================
# PHOENIX CLIENT
# ==========================================

def get_phoenix_client():

    client = Client(
        base_url=PHOENIX_BASE_URL,
        api_key=PHOENIX_API_KEY
    )

    return client


# ==========================================
# LOAD CSV DATASET
# ==========================================

def load_csv_dataset():

    print("\nLoading CSV dataset...")

    df = pd.read_csv(
        DATASET_PATH,
        dtype=str,
        keep_default_na=False
    )

    required_columns = [
        "id",
        "question",
        "ground_truth",
        "category"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing CSV columns: {missing_columns}"
        )

    df = df[required_columns].copy()

    for column in required_columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )

    if df.empty:
        raise ValueError(
            "Evaluation dataset is empty."
        )

    if (
        df["question"].eq("").any()
        or df["ground_truth"].eq("").any()
    ):
        raise ValueError(
            "Questions and ground truths cannot be empty."
        )

    if df["id"].duplicated().any():
        raise ValueError(
            "Dataset contains duplicate IDs."
        )

    print(
        f"Loaded {len(df)} evaluation examples."
    )

    return df


# ==========================================
# REGISTER PHOENIX DATASET
# ==========================================

def register_dataset(
    client,
    df
):

    print("\nRegistering dataset in Phoenix...")

    # --------------------------------------
    # GENERATE DATASET VERSION IDENTIFIER
    # --------------------------------------

    # A content hash prevents silently
    # reusing an outdated dataset after
    # the CSV has been edited.

    csv_content = (
        df.to_csv(index=False)
        .encode("utf-8")
    )

    dataset_hash = hashlib.sha256(
        csv_content
    ).hexdigest()[:12]

    dataset_name = (
        f"{PHOENIX_DATASET_NAME}-{dataset_hash}"
    )

    # --------------------------------------
    # CHECK WHETHER DATASET EXISTS
    # --------------------------------------

    existing_datasets = (
        client.datasets.list()
    )

    dataset_exists = any(
        item["name"] == dataset_name
        for item in existing_datasets
    )

    if dataset_exists:

        print(
            f"Reusing existing dataset: {dataset_name}"
        )

        return client.datasets.get_dataset(
            dataset=dataset_name
        )

    # --------------------------------------
    # PREPARE DATASET EXAMPLES
    # --------------------------------------

    inputs = []

    outputs = []

    metadata = []

    for _, row in df.iterrows():

        inputs.append({
            "question": row["question"]
        })

        outputs.append({
            "answer": row["ground_truth"]
        })

        metadata.append({
            "id": row["id"],
            "category": row["category"]
        })

    # --------------------------------------
    # CREATE DATASET IN PHOENIX
    # --------------------------------------

    dataset = client.datasets.create_dataset(
        name=dataset_name,
        inputs=inputs,
        outputs=outputs,
        metadata=metadata,
        dataset_description=(
            "BizInsight AI evaluation dataset "
            "created from CSV."
        )
    )

    print(
        f"Dataset registered: {dataset_name}"
    )

    return dataset


# ==========================================
# PHOENIX EXPERIMENT TASK
# ==========================================

def bizinsight_task(input):

    question = input["question"]

    print("\n" + "=" * 60)

    print("QUESTION:")
    print(question)

    # --------------------------------------
    # EXECUTE BIZINSIGHT
    # --------------------------------------

    result = ask(question)

    print("\nPREDICTION:")
    print(result["answer"])

    print("\nLATENCY:")
    print(result["latency"])

    return result


# ==========================================
# RUN PHOENIX EXPERIMENT
# ==========================================

def run_experiment():

    print("\n" + "=" * 70)

    print("BIZINSIGHT AI - PHOENIX EVALUATION")

    print("=" * 70)

    # --------------------------------------
    # STEP 1: CONNECT TO PHOENIX
    # --------------------------------------

    client = get_phoenix_client()

    print(
        f"\nPhoenix endpoint: {PHOENIX_BASE_URL}"
    )

    # --------------------------------------
    # STEP 2: LOAD CSV
    # --------------------------------------

    df = load_csv_dataset()

    # --------------------------------------
    # STEP 3: REGISTER DATASET
    # --------------------------------------

    dataset = register_dataset(
        client,
        df
    )

    # --------------------------------------
    # STEP 4: LOAD EVALUATORS
    # --------------------------------------

    evaluators = get_evaluators()

    print("\nRegistered evaluators:")

    for name in evaluators:
        print(f" - {name}")

    # --------------------------------------
    # STEP 5: RUN EXPERIMENT
    # --------------------------------------

    print("\nStarting Phoenix experiment...")

    experiment = client.experiments.run_experiment(
        dataset=dataset,
        task=bizinsight_task,
        evaluators=evaluators,
        experiment_name=EXPERIMENT_NAME,
        experiment_description=EXPERIMENT_DESCRIPTION,
        experiment_metadata={
            "application": "BizInsight AI",
            "evaluation_type": "LLM-as-a-Judge",
            "judge_model": JUDGE_MODEL,
            "dataset_source": "CSV"
        },
        repetitions=1,
        retries=0,
        timeout=180,
        print_summary=True
    )

    # --------------------------------------
    # STEP 6: DISPLAY RESULTS
    # --------------------------------------

    print("\n" + "=" * 70)

    print("EXPERIMENT COMPLETED")

    print("=" * 70)

    print(
        f"Experiment name: {EXPERIMENT_NAME}"
    )

    print(
        f"Dataset: {dataset.name}"
    )

    print(
        f"Total examples: {len(df)}"
    )

    return experiment
