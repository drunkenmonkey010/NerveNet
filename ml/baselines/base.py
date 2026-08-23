from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaselineModel(ABC):
    """Contract for simple, interpretable baseline models."""

    @abstractmethod
    def fit(self, X: Any, y: Any) -> BaselineModel:
        """Fit the baseline."""
        raise NotImplementedError

    @abstractmethod
    def predict(self, X: Any) -> Any:
        """Generate baseline predictions."""
        raise NotImplementedError