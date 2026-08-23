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

from ml.features.dataco import DataCoFeatureTransformer
from ml.models.logistic_regression import LogisticRegressionModel


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
    print(f"Accuracy : {accuracy_score(y_true, predictions):.4f}")
    print(f"Precision: {precision_score(y_true, predictions):.4f}")
    print(f"Recall   : {recall_score(y_true, predictions):.4f}")
    print(f"F1       : {f1_score(y_true, predictions):.4f}")
    print(f"ROC-AUC  : {roc_auc_score(y_true, probabilities):.4f}")
    print(f"Log Loss : {log_loss(y_true, probabilities):.4f}")


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

    # IMPORTANT:
    # Fit preprocessing ONLY on training data.
    transformer = DataCoFeatureTransformer()

    X_train_transformed = transformer.fit_transform(
        X_train
    )

    X_validation_transformed = transformer.transform(
        X_validation
    )

    X_test_transformed = transformer.transform(
        X_test
    )

    model = LogisticRegressionModel()

    model.fit(
        X_train_transformed,
        y_train,
    )

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

    print("=== NERVENET LOGISTIC REGRESSION ===")
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