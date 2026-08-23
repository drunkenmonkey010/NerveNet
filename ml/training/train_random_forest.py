from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)

from ml.features.dataco_tree import DataCoTreeFeatureTransformer
from ml.models.random_forest import RandomForestModel


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
    predictions,
    probabilities,
) -> None:
    print(
        f"Accuracy : "
        f"{accuracy_score(y_true, predictions):.4f}"
    )

    print(
        f"Precision: "
        f"{precision_score(y_true, predictions, zero_division=0):.4f}"
    )

    print(
        f"Recall   : "
        f"{recall_score(y_true, predictions, zero_division=0):.4f}"
    )

    print(
        f"F1       : "
        f"{f1_score(y_true, predictions, zero_division=0):.4f}"
    )

    print(
        f"ROC-AUC  : "
        f"{roc_auc_score(y_true, probabilities):.4f}"
    )

    print(
        f"Log Loss : "
        f"{log_loss(y_true, probabilities):.4f}"
    )


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

    print("=== PREPARING FEATURES ===")

    transformer = DataCoTreeFeatureTransformer()

    X_train_transformed = transformer.fit_transform(
        X_train
    )

    X_validation_transformed = transformer.transform(
        X_validation
    )

    X_test_transformed = transformer.transform(
        X_test
    )

    print(
        f"Training feature matrix: "
        f"{X_train_transformed.shape}"
    )

    print(
        f"Validation feature matrix: "
        f"{X_validation_transformed.shape}"
    )

    print(
        f"Test feature matrix: "
        f"{X_test_transformed.shape}"
    )

    print()
    print("=== TRAINING RANDOM FOREST ===")

    model = RandomForestModel(
        n_estimators=200,
        max_depth=16,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        X_train_transformed,
        y_train,
    )

    print("Training complete.")

    validation_predictions = model.predict(
        X_validation_transformed
    )

    validation_probabilities = model.predict_proba(
        X_validation_transformed
    )[:, 1]

    test_predictions = model.predict(
        X_test_transformed
    )

    test_probabilities = model.predict_proba(
        X_test_transformed
    )[:, 1]

    print()
    print("=== NERVENET RANDOM FOREST V2 ===")

    print()
    print("Training rows:", len(train))
    print("Validation rows:", len(validation))
    print("Test rows:", len(test))

    print()
    print("=== VALIDATION ===")

    evaluate(
        y_validation,
        validation_predictions,
        validation_probabilities,
    )

    print()
    print("=== TEST ===")

    evaluate(
        y_test,
        test_predictions,
        test_probabilities,
    )


if __name__ == "__main__":
    main()