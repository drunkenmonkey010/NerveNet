import pandas as pd

from ml.data.cleaning import (
    clean_data,
    validate_required_columns,
    validate_target,
)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Days for shipping (real)": [3],
            "Days for shipment (scheduled)": [4],
            "Delivery Status": ["Advance shipping"],
            "Late_delivery_risk": [0],
            "Shipping Mode": ["Standard Class"],
            "Market": ["Pacific Asia"],
            "Order Country": ["India"],
            "Order Region": ["South Asia"],
            "Order City": ["Bikaner"],
            "Customer Segment": ["Consumer"],
            "Order Item Product Price": [327.75],
            "Order Item Quantity": [1],
            "Order Item Discount": [13.11],
            "order date (DateOrders)": ["1/31/2018 22:56"],
            "shipping date (DateOrders)": ["2/3/2018 22:56"],
            "Customer Email": ["should-be-removed"],
            "Customer Password": ["should-be-removed"],
            "Customer Fname": ["should-be-removed"],
            "Customer Lname": ["should-be-removed"],
            "Customer Street": ["should-be-removed"],
            "Customer Zipcode": [12345],
            "Product Description": [None],
            "Product Image": ["should-be-removed"],
            "Order Id": [123],
        }
    )


def test_required_columns_are_valid():
    df = sample_dataframe()

    validate_required_columns(df)


def test_invalid_target_is_rejected():
    df = sample_dataframe()
    df["Late_delivery_risk"] = [2]

    try:
        validate_target(df)
    except ValueError:
        return

    raise AssertionError("Invalid target value was accepted")


def test_cleaning_removes_sensitive_columns():
    cleaned = clean_data(sample_dataframe())

    assert "Customer Email" not in cleaned.columns
    assert "Customer Password" not in cleaned.columns
    assert "Customer Street" not in cleaned.columns


def test_cleaning_parses_dates():
    cleaned = clean_data(sample_dataframe())

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned["order date (DateOrders)"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned["shipping date (DateOrders)"]
    )


def test_target_is_preserved():
    cleaned = clean_data(sample_dataframe())

    assert "Late_delivery_risk" in cleaned.columns
    assert cleaned["Late_delivery_risk"].tolist() == [0]