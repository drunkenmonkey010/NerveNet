from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class FeatureTransformer(ABC):
    """Contract for transforming raw data into model-ready features."""

    @abstractmethod
    def fit(self, data: Any) -> FeatureTransformer:
        """Learn transformation parameters from data."""
        raise NotImplementedError

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """Transform data using the fitted parameters."""
        raise NotImplementedError

    def fit_transform(self, data: Any) -> Any:
        """Fit the transformer and transform the same data."""
        self.fit(data)
        return self.transform(data)