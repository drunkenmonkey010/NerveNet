from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "interim"
    / "dataco_clean.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
)

OUTPUT_FILE = OUTPUT_DIR / "dataco_prediction.csv"


# Information available at order creation time.
PREDICTION_FEATURES = [
    "Type",
    "Days for shipment (scheduled)",
    "Category Name",
    "Customer City",
    "Customer Country",
    "Customer Segment",
    "Customer State",
    "Department Name",
    "Latitude",
    "Longitude",
    "Market",
    "Order City",
    "Order Country",
    "order date (DateOrders)",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Product Price",
    "Order Item Quantity",
    "Order Region",
    "Order State",
    "Product Name",
    "Product Price",
    "Shipping Mode",
]

TARGET = "Late_delivery_risk"


LEAKAGE_COLUMNS = [
    "Days for shipping (real)",
    "Delivery Status",
    "shipping date (DateOrders)",
    "Order Status",
]


def load_data() -> pd.DataFrame:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {INPUT_FILE}"
        )

    return pd.read_csv(INPUT_FILE)


def validate_columns(df: pd.DataFrame) -> None:
    required = set(PREDICTION_FEATURES + [TARGET])
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )


def validate_no_leakage(df: pd.DataFrame) -> None:
    present = set(df.columns)

    leakage_present = present.intersection(LEAKAGE_COLUMNS)

    if leakage_present:
        raise ValueError(
            "Leakage columns are present in prediction dataset: "
            f"{sorted(leakage_present)}"
        )


def prepare_dataset(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)

    result = df[PREDICTION_FEATURES + [TARGET]].copy()

    result["order date (DateOrders)"] = pd.to_datetime(
        result["order date (DateOrders)"],
        errors="coerce",
    )

    if result["order date (DateOrders)"].isna().any():
        raise ValueError(
            "Invalid order timestamps detected."
        )

    result = result.sort_values(
        "order date (DateOrders)"
    ).reset_index(drop=True)

    validate_no_leakage(result)

    return result


def save_dataset(df: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )


def print_summary(df: pd.DataFrame) -> None:
    print("=== PREDICTION DATASET ===")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print()
    print("=== TIME RANGE ===")
    print(f"Start: {df['order date (DateOrders)'].min()}")
    print(f"End:   {df['order date (DateOrders)'].max()}")

    print()
    print("=== TARGET ===")
    print(df[TARGET].value_counts())
    print(df[TARGET].value_counts(normalize=True))

    print()
    print("=== OUTPUT ===")
    print(OUTPUT_FILE)


def main() -> None:
    df = load_data()
    prepared = prepare_dataset(df)

    save_dataset(prepared)
    print_summary(prepared)


if __name__ == "__main__":
    main()