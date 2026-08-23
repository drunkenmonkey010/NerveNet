from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "ml" / "experiments" / "results"
OUTPUT_FILE = OUTPUT_DIR / "random_forest_v2.json"


RESULT = {
    "experiment": "random_forest_v2",
    "model": "random_forest",
    "dataset": "DataCoSupplyChainDataset",
    "target": "Late_delivery_risk",
    "prediction_time": "order_creation",
    "split": {
        "train": "2015-2016",
        "validation": "2017",
        "test": "2018-01",
        "strategy": "chronological",
    },
    "model_parameters": {
        "n_estimators": 200,
        "max_depth": 16,
        "min_samples_leaf": 2,
        "random_state": 42,
    },
    "features": {
        "numeric": [
            "Days for shipment (scheduled)",
            "Order Item Discount",
            "Order Item Discount Rate",
            "Order Item Product Price",
            "Order Item Quantity",
            "Product Price",
            "Latitude",
            "Longitude",
            "order_year",
            "order_month",
            "order_day_of_week",
            "order_hour",
        ],
        "categorical": [
            "Type",
            "Category Name",
            "Customer Segment",
            "Department Name",
            "Market",
            "Order Region",
            "Shipping Mode",
        ],
    },
    "validation": {
        "accuracy": 0.7163,
        "precision": 0.8480,
        "recall": 0.5836,
        "f1": 0.6914,
        "roc_auc": 0.7648,
        "log_loss": 0.5377,
        "brier_score": 0.1852,
    },
    "test": {
        "accuracy": 0.7197,
        "precision": 0.8614,
        "recall": 0.5983,
        "f1": 0.7062,
        "roc_auc": 0.7802,
        "log_loss": 0.5260,
        "brier_score": 0.1805,
    },
    "comparison": {
        "logistic_v1_test_roc_auc": 0.7566,
        "logistic_v1_test_log_loss": 0.5513,
        "logistic_v1_test_brier_score": 0.1901,
    },
    "notes": [
        "Random Forest outperformed Logistic Regression on the main test metrics.",
        "Prediction-time leakage columns were excluded.",
        "Preprocessing was fitted only on training data.",
        "Random Forest probabilities showed improved Brier score over Logistic Regression.",
    ],
    "recorded_at": datetime.now(
        timezone.utc
    ).isoformat(),
}


def main() -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            RESULT,
            file,
            indent=2,
        )

    print(f"Experiment recorded: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()