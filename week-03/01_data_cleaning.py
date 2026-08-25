import pandas as pd
from pathlib import Path


# ============================================================
# WEEK 03 - DATA CLEANING
# ============================================================

print("=" * 60)
print("WEEK 03 - DATA CLEANING")
print("=" * 60)


# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
CLEANED_DIR = DATA_DIR / "cleaned"

CLEANED_DIR.mkdir(parents=True, exist_ok=True)

print(f"Project root: {PROJECT_ROOT}")
print(f"Data folder: {DATA_DIR}")
print(f"Cleaned folder: {CLEANED_DIR}")


# ------------------------------------------------------------
# 2. DATASETS
# ------------------------------------------------------------

datasets = {
    "products": "products.csv",
    "inventory": "inventory_master.csv",
    "sales_orders_lines": "sales_orders_lines.csv",
    "sales_orders_header": "sales_orders_header.csv"
}


# ------------------------------------------------------------
# 3. CLEANING FUNCTION
# ------------------------------------------------------------

def clean_data(df):

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Clean text columns
    text_columns = df.select_dtypes(include=["object"]).columns

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

        df[column] = df[column].replace(
            {
                "": pd.NA,
                "nan": pd.NA,
                "None": pd.NA
            }
        )

    # Remove duplicate rows
    df = df.drop_duplicates()

    return df


# ------------------------------------------------------------
# 4. PROCESS DATASETS
# ------------------------------------------------------------

summary = []


for name, filename in datasets.items():

    print()
    print("-" * 60)
    print(f"Processing: {filename}")
    print("-" * 60)

    input_file = DATA_DIR / filename

    if not input_file.exists():
        print(f"File not found: {input_file}")
        continue

    # Load data
    df = pd.read_csv(input_file)

    original_rows = len(df)
    original_columns = len(df.columns)

    # Missing values before cleaning
    missing_before = int(df.isna().sum().sum())

    # Clean data
    df = clean_data(df)

    # Missing values after cleaning
    missing_after = int(df.isna().sum().sum())

    cleaned_rows = len(df)

    duplicates_removed = original_rows - cleaned_rows

    # Save cleaned file
    output_file = CLEANED_DIR / f"{name}_cleaned.csv"

    df.to_csv(
        output_file,
        index=False
    )

    # Store summary
    summary.append(
        {
            "dataset": name,
            "original_rows": original_rows,
            "cleaned_rows": cleaned_rows,
            "columns": original_columns,
            "duplicates_removed": duplicates_removed,
            "missing_before": missing_before,
            "missing_after": missing_after
        }
    )

    print(f"Original rows: {original_rows}")
    print(f"Cleaned rows: {cleaned_rows}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Missing values before: {missing_before}")
    print(f"Missing values after: {missing_after}")
    print(f"Saved: {output_file}")


# ------------------------------------------------------------
# 5. SAVE CLEANING SUMMARY
# ------------------------------------------------------------

summary_df = pd.DataFrame(summary)

summary_file = CLEANED_DIR / "week03_cleaning_summary.csv"

summary_df.to_csv(
    summary_file,
    index=False
)


# ------------------------------------------------------------
# 6. FINAL OUTPUT
# ------------------------------------------------------------

print()
print("=" * 60)
print("WEEK 03 - DATA CLEANING COMPLETE")
print("=" * 60)

print(f"Output directory: {CLEANED_DIR}")
print(f"Summary file: {summary_file}")