from typing import Any

from ml.datasets.base import DatasetSource


class FakeDataset(DatasetSource):
    def load(self) -> list[dict[str, Any]]:
        return [{"id": 1}]

    def validate(self, data: Any) -> None:
        if not isinstance(data, list):
            raise ValueError("Dataset must be a list")

    def metadata(self) -> dict[str, Any]:
        return {
            "name": "fake",
            "version": "1",
        }


def test_dataset_source_contract():
    dataset = FakeDataset()

    data = dataset.load()

    dataset.validate(data)

    assert data == [{"id": 1}]
    assert dataset.metadata()["name"] == "fake"