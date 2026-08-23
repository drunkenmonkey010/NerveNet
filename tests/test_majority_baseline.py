from ml.baselines.majority_class import MajorityClassBaseline


def test_majority_class_baseline():
    model = MajorityClassBaseline()

    X_train = [
        {"feature": 1},
        {"feature": 2},
        {"feature": 3},
        {"feature": 4},
    ]

    y_train = [1, 1, 1, 0]

    model.fit(X_train, y_train)

    predictions = model.predict(
        [{"feature": 10}, {"feature": 20}]
    )

    assert predictions == [1, 1]