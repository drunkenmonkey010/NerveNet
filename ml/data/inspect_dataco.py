from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "ml" / "data" / "raw"

DATA_FILE = RAW_DIR / "DataCoSupplyChainDataset.csv"


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE, encoding="latin-1")

    print("\n=== DATASET SHAPE ===")
    print(df.shape)

    print("\n=== COLUMNS ===")
    for column in df.columns:
        print(column)

    print("\n=== DATA TYPES ===")
    print(df.dtypes)

    print("\n=== MISSING VALUES ===")
    missing = df.isnull().sum()
    print(missing[missing > 0].sort_values(ascending=False))

    print("\n=== DUPLICATES ===")
    print(df.duplicated().sum())

    print("\n=== SAMPLE ===")
    print(df.head(5).to_string())

    print("\n=== TARGET CANDIDATE ===")

    if "Late_delivery_risk" in df.columns:
        print(df["Late_delivery_risk"].value_counts(dropna=False))
        print(df["Late_delivery_risk"].value_counts(normalize=True))

    print("\n=== DELIVERY STATUS ===")

    if "Delivery Status" in df.columns:
        print(df["Delivery Status"].value_counts(dropna=False))

    print("\n=== SHIPPING MODE ===")

    if "Shipping Mode" in df.columns:
        print(df["Shipping Mode"].value_counts(dropna=False))


if __name__ == "__main__":
    main()