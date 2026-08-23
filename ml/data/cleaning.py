from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
INTERIM_DIR = PROJECT_ROOT / "ml" / "data" / "interim"

INPUT_FILE = RAW_DIR / "DataCoSupplyChainDataset.csv"
OUTPUT_FILE = INTERIM_DIR / "dataco_clean.csv"


REQUIRED_COLUMNS = {
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Delivery Status",
    "Late_delivery_risk",
    "Shipping Mode",
    "Market",
    "Order Country",
    "Order Region",
    "Order City",
    "Customer Segment",
    "Order Item Product Price",
    "Order Item Quantity",
    "Order Item Discount",
    "order date (DateOrders)",
    "shipping date (DateOrders)",
}


COLUMNS_TO_REMOVE = {
    # Customer-sensitive / unnecessary information
    "Customer Email",
    "Customer Fname",
    "Customer Lname",
    "Customer Password",
    "Customer Street",
    "Customer Zipcode",
    "Order Zipcode",

    # Not useful for our first prediction problem
    "Product Description",
    "Product Image",

    # Identifiers that we don't want the first model to memorize
    "Customer Id",
    "Order Customer Id",
    "Order Id",
    "Order Item Id",
    "Order Item Cardprod Id",
    "Product Card Id",
    "Category Id",
    "Product Category Id",
    "Department Id",
}


DATE_COLUMNS = [
    "order date (DateOrders)",
    "shipping date (DateOrders)",
]


def load_raw_data() -> pd.DataFrame:
    """Load the immutable raw DataCo dataset."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {INPUT_FILE}"
        )

    return pd.read_csv(
        INPUT_FILE,
        encoding="latin-1",
    )


def validate_required_columns(df: pd.DataFrame) -> None:
    """Ensure the expected source schema is present."""
    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing)}"
        )


def remove_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove sensitive and unnecessary source columns."""
    columns_present = [
        column
        for column in COLUMNS_TO_REMOVE
        if column in df.columns
    ]

    return df.drop(columns=columns_present)


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse source timestamp columns."""
    result = df.copy()

    for column in DATE_COLUMNS:
        if column in result.columns:
            result[column] = pd.to_datetime(
                result[column],
                errors="coerce",
            )

    return result


def validate_target(df: pd.DataFrame) -> None:
    """Validate the first prediction target."""
    if "Late_delivery_risk" not in df.columns:
        raise ValueError("Late_delivery_risk target is missing")

    invalid_values = set(df["Late_delivery_risk"].dropna().unique()) - {
        0,
        1,
    }

    if invalid_values:
        raise ValueError(
            f"Unexpected target values: {sorted(invalid_values)}"
        )


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply deterministic cleaning operations."""
    validate_required_columns(df)

    result = remove_unnecessary_columns(df)
    result = parse_dates(result)

    validate_target(result)

    return result


def build_quality_report(df: pd.DataFrame) -> dict:
    """Build a lightweight data-quality report."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": {
            column: int(count)
            for column, count in df.isna().sum().items()
            if count > 0
        },
        "target_distribution": (
            df["Late_delivery_risk"]
            .value_counts(dropna=False)
            .to_dict()
            if "Late_delivery_risk" in df.columns
            else {}
        ),
    }


def save_clean_data(df: pd.DataFrame) -> None:
    """Save cleaned data to the interim layer."""
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )


def main() -> None:
    raw = load_raw_data()
    cleaned = clean_data(raw)

    report = build_quality_report(cleaned)

    save_clean_data(cleaned)

    print("=== CLEANING COMPLETE ===")
    print(f"Input:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print()
    print("=== QUALITY REPORT ===")

    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()