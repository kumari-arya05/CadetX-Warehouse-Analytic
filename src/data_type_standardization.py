import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parents[1]
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

print("=" * 60)
print("DATA TYPE STANDARDIZATION")
print("=" * 60)

# Get cleaned CSV files
csv_files = list(CLEANED_DIR.glob("*.csv"))

for file in csv_files:

    print(f"\nProcessing: {file.name}")

    df = pd.read_csv(file)

    converted_columns = []

    # Find columns containing "date"
    date_columns = [
        column
        for column in df.columns
        if "date" in column.lower()
    ]

    for column in date_columns:

        original_non_null = df[column].notna().sum()

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        converted_non_null = df[column].notna().sum()

        converted_columns.append(column)

        print(
            f"{column}: converted to datetime "
            f"({converted_non_null}/{original_non_null} valid)"
        )

    # Save standardized dataset
    df.to_csv(file, index=False)

    if converted_columns:
        print("Converted columns:", converted_columns)
    else:
        print("No date columns found.")

print("\n" + "=" * 60)
print("DATA TYPE STANDARDIZATION COMPLETED")
print("=" * 60)