from typing import Any

from ml.features.base import FeatureTransformer


class FakeFeatureTransformer(FeatureTransformer):
    def __init__(self) -> None:
        self.fitted = False

    def fit(self, data: Any) -> FeatureTransformer:
        self.fitted = True
        return self

    def transform(self, data: Any) -> Any:
        if not self.fitted:
            raise RuntimeError("Transformer has not been fitted")

        return data


def test_feature_transformer_contract():
    transformer = FakeFeatureTransformer()

    data = [{"delay": 10}]

    result = transformer.fit_transform(data)

    assert result == data
    assert transformer.fitted is True