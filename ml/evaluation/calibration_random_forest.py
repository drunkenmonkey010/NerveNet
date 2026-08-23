from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss

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


def print_calibration(
    y_true: pd.Series,
    probabilities,
) -> None:
    fraction, mean = calibration_curve(
        y_true,
        probabilities,
        n_bins=10,
        strategy="quantile",
    )

    for predicted, actual in zip(
        mean,
        fraction,
    ):
        print(
            f"Predicted={predicted:.3f} "
            f"Actual={actual:.3f}"
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

    print("=== RANDOM FOREST V2 CALIBRATION ===")
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

    print_calibration(
        y_validation,
        validation_probabilities,
    )

    print()
    print("=== TEST CALIBRATION ===")

    print_calibration(
        y_test,
        test_probabilities,
    )


if __name__ == "__main__":
    main()