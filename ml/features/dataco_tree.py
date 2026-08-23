from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from ml.features.base import FeatureTransformer
from ml.features.dataco import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TIME_FEATURES,
    DATE_COLUMN,
)


class DataCoTreeFeatureTransformer(FeatureTransformer):
    """DataCo feature transformer for tree-based models."""

    def __init__(self) -> None:
        self.preprocessor: ColumnTransformer | None = None

    def _add_time_features(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        result = data.copy()

        timestamps = pd.to_datetime(
            result[DATE_COLUMN],
            errors="coerce",
        )

        if timestamps.isna().any():
            raise ValueError(
                "Invalid order timestamps detected."
            )

        result["order_year"] = timestamps.dt.year
        result["order_month"] = timestamps.dt.month
        result["order_day_of_week"] = timestamps.dt.dayofweek
        result["order_hour"] = timestamps.dt.hour

        return result

    def _build_preprocessor(self) -> ColumnTransformer:
        return ColumnTransformer(
            transformers=[
                (
                    "numeric",
                    "passthrough",
                    NUMERIC_FEATURES + TIME_FEATURES,
                ),
                (
                    "categorical",
                    OneHotEncoder(
                        handle_unknown="ignore",
                    ),
                    CATEGORICAL_FEATURES,
                ),
            ],
            remainder="drop",
        )

    def fit(self, data: pd.DataFrame, y=None):
        prepared = self._add_time_features(data)

        self.preprocessor = self._build_preprocessor()

        self.preprocessor.fit(prepared)

        return self

    def transform(self, data: pd.DataFrame):
        if self.preprocessor is None:
            raise RuntimeError(
                "Feature transformer has not been fitted."
            )

        prepared = self._add_time_features(data)

        return self.preprocessor.transform(prepared)

    def fit_transform(self, data: pd.DataFrame, y=None):
        prepared = self._add_time_features(data)

        self.preprocessor = self._build_preprocessor()

        return self.preprocessor.fit_transform(prepared)