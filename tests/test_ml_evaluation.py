from typing import Any

from ml.evaluation.base import EvaluationResult, Evaluator


class FakeEvaluator(Evaluator):
    def evaluate(
        self,
        y_true: Any,
        y_pred: Any,
    ) -> list[EvaluationResult]:
        return [
            EvaluationResult(
                metric_name="fake_accuracy",
                metric_value=1.0,
                metadata={"dataset": "test"},
            )
        ]


def test_evaluation_result():
    result = EvaluationResult(
        metric_name="accuracy",
        metric_value=0.95,
    )

    assert result.metric_name == "accuracy"
    assert result.metric_value == 0.95
    assert result.metadata == {}


def test_evaluator_contract():
    evaluator = FakeEvaluator()

    results = evaluator.evaluate(
        y_true=[1, 0, 1],
        y_pred=[1, 0, 1],
    )

    assert len(results) == 1
    assert results[0].metric_name == "fake_accuracy"
    assert results[0].metric_value == 1.0
    assert results[0].metadata["dataset"] == "test"