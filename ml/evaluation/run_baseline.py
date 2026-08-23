from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from ml.baselines.majority_class import MajorityClassBaseline


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SPLIT_DIR = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "splits"
)

TARGET = "Late_delivery_risk"


def load_split(name: str) -> pd.DataFrame:
    path = SPLIT_DIR / f"{name}.csv"

    if not path.exists():
        raise FileNotFoundError(
            f"Split not found: {path}"
        )

    return pd.read_csv(path)


def evaluate(
    y_true: pd.Series,
    y_pred: list[int],
) -> None:
    print("Accuracy :", accuracy_score(y_true, y_pred))
    print("Precision:", precision_score(y_true, y_pred, zero_division=0))
    print("Recall   :", recall_score(y_true, y_pred, zero_division=0))
    print("F1       :", f1_score(y_true, y_pred, zero_division=0))

    print()
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))


def main() -> None:
    train = load_split("train")
    validation = load_split("validation")
    test = load_split("test")

    X_train = train.drop(columns=[TARGET])
    y_train = train[TARGET]

    X_validation = validation.drop(columns=[TARGET])
    y_validation = validation[TARGET]

    X_test = test.drop(columns=[TARGET])
    y_test = test[TARGET]

    model = MajorityClassBaseline()

    model.fit(
        X_train,
        y_train,
    )

    print("=== MAJORITY BASELINE ===")
    print(f"Training rows:   {len(train)}")
    print(f"Validation rows: {len(validation)}")
    print(f"Test rows:       {len(test)}")
    print()

    print("=== VALIDATION ===")

    validation_predictions = model.predict(
        X_validation
    )

    evaluate(
        y_validation,
        validation_predictions,
    )

    print()
    print("=== TEST ===")

    test_predictions = model.predict(
        X_test
    )

    evaluate(
        y_test,
        test_predictions,
    )


if __name__ == "__main__":
    main()