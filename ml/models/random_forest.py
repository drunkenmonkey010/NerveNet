from __future__ import annotations

from typing import Any

from sklearn.ensemble import RandomForestClassifier

from ml.models.base import Model


class RandomForestModel(Model):
    """Random Forest classifier for shipment late-delivery risk."""

    def __init__(
        self,
        n_estimators: int = 200,
        max_depth: int | None = 16,
        min_samples_leaf: int = 2,
        random_state: int = 42,
        n_jobs: int = -1,
    ) -> None:
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state,
            n_jobs=n_jobs,
        )

    def fit(
        self,
        X: Any,
        y: Any,
    ) -> RandomForestModel:
        self.model.fit(X, y)
        return self

    def predict(self, X: Any) -> Any:
        return self.model.predict(X)

    def predict_proba(self, X: Any) -> Any:
        return self.model.predict_proba(X)

    def save(self, path) -> None:
        import joblib

        joblib.dump(self.model, path)

    @classmethod
    def load(cls, path) -> RandomForestModel:
        import joblib

        instance = cls()
        instance.model = joblib.load(path)
        return instance