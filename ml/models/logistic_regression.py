from __future__ import annotations

from typing import Any

from sklearn.linear_model import LogisticRegression

from ml.models.base import Model


class LogisticRegressionModel(Model):
    """Logistic regression classifier for binary shipment risk."""

    def __init__(
        self,
        max_iter: int = 1000,
        random_state: int = 42,
    ) -> None:
        self.model = LogisticRegression(
            max_iter=max_iter,
            random_state=random_state,
        )

    def fit(
        self,
        X: Any,
        y: Any,
    ) -> LogisticRegressionModel:
        self.model.fit(X, y)

        return self

    def predict(
        self,
        X: Any,
    ) -> Any:
        return self.model.predict(X)

    def predict_proba(
        self,
        X: Any,
    ) -> Any:
        return self.model.predict_proba(X)

    def save(self, path) -> None:
        import joblib

        joblib.dump(self.model, path)

    @classmethod
    def load(cls, path) -> LogisticRegressionModel:
        import joblib

        instance = cls()
        instance.model = joblib.load(path)

        return instance