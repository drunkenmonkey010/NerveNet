# Learning Loop

See [../../NERVENET_PRODUCT_SPEC.md](../../NERVENET_PRODUCT_SPEC.md), especially sections 7, 10, 14, and 19.

The core loop is:

Observation -> Prediction -> Decision -> Outcome -> Evaluation -> Memory -> Model training -> Belief update

NerveNet should compare predicted outcomes to actual outcomes, store relevant evidence, update agent memories and beliefs, and use validated datasets for retraining. The first versions should use clear baselines before introducing complex ML.
