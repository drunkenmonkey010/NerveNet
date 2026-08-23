from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "ml" / "experiments" / "results"
OUTPUT_FILE = OUTPUT_DIR / "logistic_v1.json"


RESULT = {
    "experiment": "logistic_v1",
    "model": "logistic_regression",
    "dataset": "DataCoSupplyChainDataset",
    "target": "Late_delivery_risk",
    "prediction_time": "order_creation",
    "split": {
        "train": "2015-2016",
        "validation": "2017",
        "test": "2018-01",
        "strategy": "chronological",
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
        "accuracy": 0.6968,
        "precision": 0.8429,
        "recall": 0.5447,
        "f1": 0.6617,
        "roc_auc": 0.7381,
        "log_loss": 0.5715,
        "brier_score": 0.1973,
    },
    "test": {
        "accuracy": 0.7056,
        "precision": 0.8617,
        "recall": 0.5682,
        "f1": 0.6848,
        "roc_auc": 0.7566,
        "log_loss": 0.5513,
        "brier_score": 0.1901,
    },
    "baseline": {
        "test_accuracy": 0.5629,
        "test_f1": 0.7203,
    },
    "notes": [
        "Prediction-time leakage columns were excluded.",
        "Preprocessing was fitted only on training data.",
        "Shipping Mode is the strongest feature.",
        "Shipping Mode and scheduled shipment duration are strongly related.",
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