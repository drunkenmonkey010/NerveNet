from pathlib import Path
from typing import Any

from ml.models.base import Model


class FakeModel(Model):
    def __init__(self) -> None:
        self.fitted = False

    def fit(self, X: Any, y: Any) -> Model:
        self.fitted = True
        return self

    def predict(self, X: Any) -> list[int]:
        if not self.fitted:
            raise RuntimeError("Model has not been fitted")

        return [1 for _ in X]

    def save(self, path: Path) -> None:
        path.write_text("fake-model", encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> Model:
        if not path.exists():
            raise FileNotFoundError(path)

        return cls()


def test_model_contract(tmp_path: Path):
    model = FakeModel()

    X = [{"feature": 1}, {"feature": 2}]
    y = [1, 0]

    model.fit(X, y)

    predictions = model.predict(X)

    assert model.fitted is True
    assert predictions == [1, 1]

    model_path = tmp_path / "model.bin"
    model.save(model_path)

    assert model_path.exists()

    loaded = FakeModel.load(model_path)

    assert isinstance(loaded, FakeModel)