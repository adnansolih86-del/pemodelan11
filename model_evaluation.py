import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


@dataclass
class EvaluationResults:
    accuracy: float
    precision_macro: float
    recall_macro: float
    f1_macro: float
    precision_weighted: float
    recall_weighted: float
    f1_weighted: float
    classification_report: str
    confusion_matrix: np.ndarray
    labels: List[str]

    def to_dict(self) -> Dict:
        return {
            "accuracy": self.accuracy,
            "precision_macro": self.precision_macro,
            "recall_macro": self.recall_macro,
            "f1_macro": self.f1_macro,
            "precision_weighted": self.precision_weighted,
            "recall_weighted": self.recall_weighted,
            "f1_weighted": self.f1_weighted,
            "classification_report": self.classification_report,
            "confusion_matrix": self.confusion_matrix.tolist(),
            "labels": self.labels,
        }


def evaluate_classification(
    y_true: List[str],
    y_pred: List[str],
    labels: Optional[List[str]] = None,
) -> EvaluationResults:
    """Evaluate classification results using standard metrics."""
    if labels is None:
        labels = sorted(list(set(y_true) | set(y_pred)))

    accuracy = accuracy_score(y_true, y_pred)
    precision_macro = precision_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)
    recall_macro = recall_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)
    f1_macro = f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)
    precision_weighted = precision_score(y_true, y_pred, labels=labels, average="weighted", zero_division=0)
    recall_weighted = recall_score(y_true, y_pred, labels=labels, average="weighted", zero_division=0)
    f1_weighted = f1_score(y_true, y_pred, labels=labels, average="weighted", zero_division=0)
    report = classification_report(y_true, y_pred, labels=labels, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    return EvaluationResults(
        accuracy=accuracy,
        precision_macro=precision_macro,
        recall_macro=recall_macro,
        f1_macro=f1_macro,
        precision_weighted=precision_weighted,
        recall_weighted=recall_weighted,
        f1_weighted=f1_weighted,
        classification_report=report,
        confusion_matrix=cm,
        labels=labels,
    )


def load_ground_truth_stance(path: str) -> pd.DataFrame:
    """Load a ground truth stance file from CSV."""
    df = pd.read_csv(path)
    required_cols = [
        "comment_id",
        "model_prediction",
        "expert_stance",
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in ground truth stance file: {missing}")
    return df


def evaluate_stance_ground_truth(
    path: str,
    prediction_col: str = "model_prediction",
    label_col: str = "expert_stance",
    label_order: Optional[List[str]] = None,
) -> EvaluationResults:
    """Evaluate stance classification using a ground truth CSV file."""
    df = load_ground_truth_stance(path)
    y_true = df[label_col].astype(str).tolist()
    y_pred = df[prediction_col].astype(str).tolist()

    labels = label_order if label_order is not None else sorted(list(set(y_true) | set(y_pred)))
    return evaluate_classification(y_true, y_pred, labels=labels)


def save_evaluation_results(results: EvaluationResults, path: str) -> None:
    """Save evaluation results to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results.to_dict(), f, indent=2, ensure_ascii=False)


def format_confusion_matrix(results: EvaluationResults) -> str:
    """Return a printable confusion matrix table."""
    labels = results.labels
    cm = results.confusion_matrix.tolist()
    header = [" "] + [f"Pred:{label}" for label in labels]
    rows = [header]
    for label, row in zip(labels, cm):
        rows.append([f"True:{label}"] + [str(int(x)) for x in row])

    col_widths = [max(len(cell) for cell in column) for column in zip(*rows)]
    lines = []
    for row in rows:
        padded = [cell.ljust(width) for cell, width in zip(row, col_widths)]
        lines.append(" | ".join(padded))
    return "\n".join(lines)


def summary_text(results: EvaluationResults) -> str:
    """Return a plain text summary of evaluation metrics."""
    return (
        f"Accuracy: {results.accuracy:.4f}\n"
        f"Precision (macro): {results.precision_macro:.4f}\n"
        f"Recall (macro): {results.recall_macro:.4f}\n"
        f"F1 Score (macro): {results.f1_macro:.4f}\n"
        f"Precision (weighted): {results.precision_weighted:.4f}\n"
        f"Recall (weighted): {results.recall_weighted:.4f}\n"
        f"F1 Score (weighted): {results.f1_weighted:.4f}\n"
    )
