from typing import Any

from ml.baselines.base import BaselineModel


class FakeBaseline(BaselineModel):
    def __init__(self) -> None:
        self.fitted = False

    def fit(self, X: Any, y: Any) -> BaselineModel:
        self.fitted = True
        return self

    def predict(self, X: Any) -> list[float]:
        if not self.fitted:
            raise RuntimeError("Baseline has not been fitted")

        return [0.5 for _ in X]


def test_baseline_contract():
    baseline = FakeBaseline()

    X = [{"feature": 1}, {"feature": 2}]
    y = [1, 0]

    baseline.fit(X, y)

    predictions = baseline.predict(X)

    assert baseline.fitted is True
    assert predictions == [0.5, 0.5]