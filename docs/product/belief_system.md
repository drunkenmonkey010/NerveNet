# Belief System

See [../../NERVENET_PRODUCT_SPEC.md](../../NERVENET_PRODUCT_SPEC.md), especially sections 6, 9, 10, and 11.

NerveNet separates world state from agent belief. A fact can be globally true while each agent maintains a different estimate because agents observe different evidence and have different histories.

A conceptual belief may include subject, predicate, value, confidence, evidence, source, timestamp, context, and last_updated. These fields are not final database schemas.

Early belief updates should use simple deterministic or statistical baselines. ML-supported belief updates should come later, after outcomes, evidence quality, and evaluation metrics are available.
