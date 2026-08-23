from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EvaluationResult:
    """A single evaluation metric result."""

    metric_name: str
    metric_value: float
    metadata: dict[str, Any] = field(default_factory=dict)


class Evaluator(ABC):
    """Contract for evaluating model predictions."""

    @abstractmethod
    def evaluate(
        self,
        y_true: Any,
        y_pred: Any,
    ) -> list[EvaluationResult]:
        """Evaluate predictions and return metric results."""
        raise NotImplementedError