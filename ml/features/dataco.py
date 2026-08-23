from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml.features.base import FeatureTransformer


DATE_COLUMN = "order date (DateOrders)"

NUMERIC_FEATURES = [
    "Days for shipment (scheduled)",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Product Price",
    "Order Item Quantity",
    "Product Price",
    "Latitude",
    "Longitude",
]

CATEGORICAL_FEATURES = [
    "Type",
    "Category Name",
    "Customer Segment",
    "Department Name",
    "Market",
    "Order Region",
    "Shipping Mode",
]

TIME_FEATURES = [
    "order_year",
    "order_month",
    "order_day_of_week",
    "order_hour",
]


class DataCoFeatureTransformer(FeatureTransformer):
    """Feature transformer for the first DataCo prediction model."""

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
                    StandardScaler(),
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

    def fit(
        self,
        data: pd.DataFrame,
        y: Any = None,
    ) -> DataCoFeatureTransformer:
        prepared = self._add_time_features(data)

        self.preprocessor = self._build_preprocessor()

        self.preprocessor.fit(prepared)

        return self

    def transform(
        self,
        data: pd.DataFrame,
    ) -> Any:
        if self.preprocessor is None:
            raise RuntimeError(
                "Feature transformer has not been fitted."
            )

        prepared = self._add_time_features(data)

        return self.preprocessor.transform(prepared)

    def fit_transform(
        self,
        data: pd.DataFrame,
        y: Any = None,
    ) -> Any:
        prepared = self._add_time_features(data)

        self.preprocessor = self._build_preprocessor()

        return self.preprocessor.fit_transform(prepared)