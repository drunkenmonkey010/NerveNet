from __future__ import annotations

from typing import Any

from ml.baselines.base import BaselineModel


class MajorityClassBaseline(BaselineModel):
    """Predict the most frequent class observed during training."""

    def __init__(self) -> None:
        self.majority_class: int | None = None

    def fit(self, X: Any, y: Any) -> MajorityClassBaseline:
        values = list(y)

        if not values:
            raise ValueError("Training target cannot be empty.")

        counts: dict[int, int] = {}

        for value in values:
            value = int(value)
            counts[value] = counts.get(value, 0) + 1

        self.majority_class = max(
            counts,
            key=counts.get,
        )

        return self

    def predict(self, X: Any) -> list[int]:
        if self.majority_class is None:
            raise RuntimeError(
                "Baseline has not been fitted."
            )

        return [
            self.majority_class
            for _ in range(len(X))
        ]