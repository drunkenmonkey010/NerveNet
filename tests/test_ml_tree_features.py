from tests.test_ml_dataco_features import sample_data

from ml.features.dataco_tree import DataCoTreeFeatureTransformer


def test_tree_transformer():
    transformer = DataCoTreeFeatureTransformer()

    transformed = transformer.fit_transform(
        sample_data()
    )

    assert transformed.shape[0] == 2
    assert transformed.shape[1] > 0


def test_tree_transformer_handles_unknown_category():
    train = sample_data()

    transformer = DataCoTreeFeatureTransformer()
    transformer.fit(train)

    test = sample_data()
    test.loc[0, "Shipping Mode"] = "Future Mode"

    transformed = transformer.transform(test)

    assert transformed.shape[0] == 2
    