from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "dataco_prediction.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "splits"
)

TRAIN_FILE = OUTPUT_DIR / "train.csv"
VALIDATION_FILE = OUTPUT_DIR / "validation.csv"
TEST_FILE = OUTPUT_DIR / "test.csv"

DATE_COLUMN = "order date (DateOrders)"

TRAIN_END_YEAR = 2016
VALIDATION_YEAR = 2017
TEST_YEAR = 2018


def load_prediction_data() -> pd.DataFrame:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Prediction dataset not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    df[DATE_COLUMN] = pd.to_datetime(
        df[DATE_COLUMN],
        errors="coerce",
    )

    if df[DATE_COLUMN].isna().any():
        raise ValueError("Invalid timestamps found.")

    return df.sort_values(DATE_COLUMN).reset_index(drop=True)


def create_temporal_split(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    years = df[DATE_COLUMN].dt.year

    train = df[years <= TRAIN_END_YEAR].copy()

    validation = df[
        years == VALIDATION_YEAR
    ].copy()

    test = df[
        years == TEST_YEAR
    ].copy()

    if train.empty:
        raise ValueError("Training split is empty.")

    if validation.empty:
        raise ValueError("Validation split is empty.")

    if test.empty:
        raise ValueError("Test split is empty.")

    return train, validation, test


def save_splits(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    train.to_csv(TRAIN_FILE, index=False)
    validation.to_csv(VALIDATION_FILE, index=False)
    test.to_csv(TEST_FILE, index=False)


def print_summary(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    test: pd.DataFrame,
) -> None:

    print("=== TEMPORAL SPLIT ===")

    for name, df in [
        ("TRAIN", train),
        ("VALIDATION", validation),
        ("TEST", test),
    ]:
        print()
        print(name)
        print(f"Rows: {len(df)}")
        print(
            f"Start: {df[DATE_COLUMN].min()}"
        )
        print(
            f"End:   {df[DATE_COLUMN].max()}"
        )

        print("Target:")
        print(
            df["Late_delivery_risk"]
            .value_counts(normalize=True)
        )


def main() -> None:
    df = load_prediction_data()

    train, validation, test = create_temporal_split(df)

    save_splits(
        train,
        validation,
        test,
    )

    print_summary(
        train,
        validation,
        test,
    )


if __name__ == "__main__":
    main()