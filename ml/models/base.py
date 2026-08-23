from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Model(ABC):
    """Contract for NerveNet ML models."""

    @abstractmethod
    def fit(self, X: Any, y: Any) -> Model:
        """Train the model."""
        raise NotImplementedError

    @abstractmethod
    def predict(self, X: Any) -> Any:
        """Generate predictions."""
        raise NotImplementedError

    @abstractmethod
    def save(self, path: Path) -> None:
        """Persist the trained model."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load(cls, path: Path) -> Model:
        """Load a previously persisted model."""
        raise NotImplementedError