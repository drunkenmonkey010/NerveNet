import pandas as pd
import pytest

from ml.data.split import create_temporal_split


DATE_COLUMN = "order date (DateOrders)"


def test_temporal_split():
    df = pd.DataFrame(
        {
            DATE_COLUMN: pd.to_datetime(
                [
                    "2015-01-01",
                    "2016-06-01",
                    "2017-01-01",
                    "2017-12-01",
                    "2018-01-01",
                ]
            ),
            "Late_delivery_risk": [
                0,
                1,
                0,
                1,
                0,
            ],
        }
    )

    train, validation, test = create_temporal_split(df)

    assert len(train) == 2
    assert len(validation) == 2
    assert len(test) == 1

    assert train[DATE_COLUMN].dt.year.max() == 2016
    assert validation[DATE_COLUMN].dt.year.unique().tolist() == [2017]
    assert test[DATE_COLUMN].dt.year.unique().tolist() == [2018]


def test_temporal_split_rejects_empty_split():
    df = pd.DataFrame(
        {
            DATE_COLUMN: pd.to_datetime(
                ["2015-01-01"]
            ),
            "Late_delivery_risk": [0],
        }
    )

    with pytest.raises(ValueError):
        create_temporal_split(df)