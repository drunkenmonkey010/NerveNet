import pandas as pd
import pytest

from ml.data.prepare_prediction_dataset import (
    LEAKAGE_COLUMNS,
    PREDICTION_FEATURES,
    TARGET,
    prepare_dataset,
)


def sample_dataframe() -> pd.DataFrame:
    data = {}

    for column in PREDICTION_FEATURES:
        if column == "order date (DateOrders)":
            data[column] = [
                "2018-01-02 10:00:00",
                "2018-01-01 10:00:00",
            ]
        elif column in {
            "Days for shipment (scheduled)",
            "Order Item Quantity",
        }:
            data[column] = [4, 3]
        elif column in {
            "Latitude",
            "Longitude",
            "Order Item Discount",
            "Order Item Discount Rate",
            "Order Item Product Price",
            "Product Price",
        }:
            data[column] = [10.0, 20.0]
        else:
            data[column] = ["value_a", "value_b"]

    data[TARGET] = [1, 0]

    return pd.DataFrame(data)


def test_prediction_dataset_keeps_target():
    result = prepare_dataset(sample_dataframe())

    assert TARGET in result.columns


def test_prediction_dataset_contains_only_prediction_features_and_target():
    result = prepare_dataset(sample_dataframe())

    assert set(result.columns) == set(
        PREDICTION_FEATURES + [TARGET]
    )


def test_prediction_dataset_is_chronologically_sorted():
    result = prepare_dataset(sample_dataframe())

    timestamps = result["order date (DateOrders)"]

    assert timestamps.is_monotonic_increasing


def test_prediction_dataset_rejects_missing_columns():
    df = sample_dataframe()

    df = df.drop(columns=[PREDICTION_FEATURES[0]])

    with pytest.raises(ValueError):
        prepare_dataset(df)


def test_leakage_columns_are_not_prediction_features():
    assert not set(LEAKAGE_COLUMNS).intersection(
        PREDICTION_FEATURES
    )