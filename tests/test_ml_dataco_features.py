import pandas as pd
import pytest

from ml.features.dataco import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    DataCoFeatureTransformer,
)


def sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Days for shipment (scheduled)": [4, 3],
            "Order Item Discount": [10.0, 20.0],
            "Order Item Discount Rate": [0.05, 0.10],
            "Order Item Product Price": [100.0, 200.0],
            "Order Item Quantity": [1, 2],
            "Product Price": [100.0, 200.0],
            "Latitude": [20.0, 30.0],
            "Longitude": [-70.0, -80.0],
            "Type": ["DEBIT", "CASH"],
            "Category Name": ["Cleats", "Smart watch"],
            "Customer Segment": ["Consumer", "Corporate"],
            "Department Name": ["Fitness", "Fan Shop"],
            "Market": ["LATAM", "Pacific Asia"],
            "Order Region": ["Caribbean", "South Asia"],
            "Shipping Mode": ["Standard Class", "First Class"],
            "order date (DateOrders)": [
                "2017-01-01 10:00:00",
                "2017-06-15 18:00:00",
            ],
        }
    )


def test_feature_transformer_fits():
    transformer = DataCoFeatureTransformer()

    transformed = transformer.fit_transform(
        sample_data()
    )

    assert transformed.shape[0] == 2
    assert transformed.shape[1] > len(
        NUMERIC_FEATURES
    )


def test_feature_transformer_handles_unseen_category():
    transformer = DataCoFeatureTransformer()

    train = sample_data()

    transformer.fit(train)

    test = sample_data()

    test.loc[0, "Shipping Mode"] = "New Future Mode"

    transformed = transformer.transform(test)

    assert transformed.shape[0] == 2


def test_transform_requires_fit():
    transformer = DataCoFeatureTransformer()

    with pytest.raises(RuntimeError):
        transformer.transform(sample_data())


def test_expected_feature_groups_are_defined():
    assert len(NUMERIC_FEATURES) == 8
    assert len(CATEGORICAL_FEATURES) == 7