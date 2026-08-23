from __future__ import annotations

from pathlib import Path

import pandas as pd

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
        raise FileNotFoundError(path)

    return pd.read_csv(path)


def main() -> None:
    train = load_split("train")

    X_train = train.drop(columns=[TARGET])
    y_train = train[TARGET]

    transformer = DataCoFeatureTransformer()

    X_train_transformed = transformer.fit_transform(
        X_train
    )

    model = LogisticRegressionModel()

    model.fit(
        X_train_transformed,
        y_train,
    )

    preprocessor = transformer.preprocessor

    if preprocessor is None:
        raise RuntimeError(
            "Feature transformer was not fitted."
        )

    feature_names = preprocessor.get_feature_names_out()

    coefficients = model.model.coef_[0]

    importance = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": coefficients,
            "absolute_coefficient": abs(coefficients),
        }
    )

    importance = importance.sort_values(
        "absolute_coefficient",
        ascending=False,
    )

    print("=== TOP 30 FEATURES ===")
    print(
        importance.head(30).to_string(index=False)
    )


if __name__ == "__main__":
    main()