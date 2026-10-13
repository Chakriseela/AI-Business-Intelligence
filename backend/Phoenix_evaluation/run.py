from backend.Phonenix_evaluation.experiment import run_experiment
from backend.config.settings import DATASET_PATH 

def main():
    # Run the experiment with the specified dataset path

    print(f"Running experiment with dataset: {DATASET_PATH}")
    print()

    print("="*70)
    print("BizInsight AI - Experiment Runner")
    print("="*70)

    run_experiment(DATASET_PATH)

if __name__ == "__main__":
    main()