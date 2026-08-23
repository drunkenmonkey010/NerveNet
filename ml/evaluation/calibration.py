from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss

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

    validation_probabilities = model.predict_proba(
        X_validation_transformed
    )[:, 1]

    test_probabilities = model.predict_proba(
        X_test_transformed
    )[:, 1]

    validation_brier = brier_score_loss(
        y_validation,
        validation_probabilities,
    )

    test_brier = brier_score_loss(
        y_test,
        test_probabilities,
    )

    print("=== PROBABILITY CALIBRATION ===")
    print()
    print(
        f"Validation Brier Score: "
        f"{validation_brier:.4f}"
    )
    print(
        f"Test Brier Score: "
        f"{test_brier:.4f}"
    )

    print()
    print("=== VALIDATION CALIBRATION ===")

    validation_fraction, validation_mean = calibration_curve(
        y_validation,
        validation_probabilities,
        n_bins=10,
        strategy="quantile",
    )

    for predicted, actual in zip(
        validation_mean,
        validation_fraction,
    ):
        print(
            f"Predicted={predicted:.3f} "
            f"Actual={actual:.3f}"
        )

    print()
    print("=== TEST CALIBRATION ===")

    test_fraction, test_mean = calibration_curve(
        y_test,
        test_probabilities,
        n_bins=10,
        strategy="quantile",
    )

    for predicted, actual in zip(
        test_mean,
        test_fraction,
    ):
        print(
            f"Predicted={predicted:.3f} "
            f"Actual={actual:.3f}"
        )


if __name__ == "__main__":
    main()