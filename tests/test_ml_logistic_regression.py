import numpy as np

from ml.models.logistic_regression import LogisticRegressionModel


def test_logistic_regression_model():
    X = np.array(
        [
            [0.0],
            [1.0],
            [2.0],
            [3.0],
        ]
    )

    y = np.array([0, 0, 1, 1])

    model = LogisticRegressionModel()

    model.fit(X, y)

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)

    assert len(predictions) == 4
    assert probabilities.shape == (4, 2)
    assert np.all(probabilities >= 0)
    assert np.all(probabilities <= 1)