from ml.experiments.base import Experiment


def test_experiment_metadata():
    experiment = Experiment(
        name="test-experiment",
        dataset_id="dataset-v1",
        model_id="model-v1",
        config={
            "seed": 42,
        },
        metrics={
            "accuracy": 0.95,
        },
        artifact_refs=[
            "models/model-v1",
        ],
    )

    assert experiment.name == "test-experiment"
    assert experiment.dataset_id == "dataset-v1"
    assert experiment.model_id == "model-v1"
    assert experiment.config["seed"] == 42
    assert experiment.metrics["accuracy"] == 0.95
    assert experiment.artifact_refs == ["models/model-v1"]
    assert experiment.created_at.tzinfo is not None