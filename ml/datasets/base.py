from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class DatasetSource(ABC):
    """Contract for datasets used by NerveNet ML pipelines."""

    @abstractmethod
    def load(self) -> Any:
        """Load and return the dataset."""
        raise NotImplementedError

    @abstractmethod
    def validate(self, data: Any) -> None:
        """Validate the dataset structure and contents."""
        raise NotImplementedError

    @abstractmethod
    def metadata(self) -> dict[str, Any]:
        """Return metadata describing the dataset."""
        raise NotImplementedError