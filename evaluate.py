import argparse
from pathlib import Path

from model_evaluation import evaluate_stance_ground_truth, format_confusion_matrix, save_evaluation_results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate stance classification using a ground truth CSV file."
    )
    parser.add_argument(
        "ground_truth",
        type=Path,
        help="Path to the ground truth stance CSV file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evaluation_results.json"),
        help="Path to save the evaluation results JSON",
    )
    parser.add_argument(
        "--labels",
        nargs="*",
        default=["POSITIVE", "NEGATIVE", "NEUTRAL"],
        help="Optional label order for evaluation",
    )
    args = parser.parse_args()

    if not args.ground_truth.exists():
        raise FileNotFoundError(f"Ground truth file not found: {args.ground_truth}")

    results = evaluate_stance_ground_truth(
        str(args.ground_truth),
        prediction_col="model_prediction",
        label_col="expert_stance",
        label_order=args.labels,
    )

    print("=== EVALUATION SUMMARY ===")
    print(results.summary_text())
    print("=== CONFUSION MATRIX ===")
    print(format_confusion_matrix(results))
    print("=== CLASSIFICATION REPORT ===")
    print(results.classification_report)

    save_evaluation_results(results, str(args.output))
    print(f"Saved evaluation results to: {args.output}")


if __name__ == "__main__":
    main()
