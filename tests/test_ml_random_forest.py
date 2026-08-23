import numpy as np

from ml.models.random_forest import RandomForestModel


def test_random_forest_model():
    X = np.array(
        [
            [0.0],
            [1.0],
            [2.0],
            [3.0],
            [4.0],
            [5.0],
        ]
    )

    y = np.array([0, 0, 0, 1, 1, 1])

    model = RandomForestModel(
        n_estimators=20,
        random_state=42,
    )

    model.fit(X, y)

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)

    assert len(predictions) == 6
    assert probabilities.shape == (6, 2)
    assert np.all(probabilities >= 0)
    assert np.all(probabilities <= 1)