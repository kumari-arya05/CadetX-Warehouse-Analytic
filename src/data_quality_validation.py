import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parents[1]
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

print("=" * 60)
print("DATA QUALITY VALIDATION")
print("=" * 60)

csv_files = list(CLEANED_DIR.glob("*.csv"))

total_files = 0
files_with_missing = 0
files_with_duplicates = 0

for file in csv_files:

    total_files += 1

    print("\n" + "-" * 60)
    print(f"FILE: {file.name}")
    print("-" * 60)

    df = pd.read_csv(file)

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    # Missing values
    missing_values = df.isnull().sum()
    total_missing = missing_values.sum()

    print("\nTotal Missing Values:", total_missing)

    if total_missing > 0:
        files_with_missing += 1
        print("Columns with missing values:")
        print(missing_values[missing_values > 0])
    else:
        print("Missing Values: 0")

    # Duplicate rows
    duplicates = df.duplicated().sum()

    print("\nDuplicate Rows:", duplicates)

    if duplicates > 0:
        files_with_duplicates += 1

    # Date validation
    date_columns = [
        column
        for column in df.columns
        if "date" in column.lower()
    ]

    if date_columns:
        print("\nDate Column Validation:")

        for column in date_columns:

            converted_dates = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            invalid_dates = (
                converted_dates.isna() &
                df[column].notna()
            ).sum()

            print(
                f"{column}: "
                f"{invalid_dates} invalid dates"
            )

    else:
        print("\nDate Column Validation: No date columns")

print("\n" + "=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)

print("Total CSV files checked:", total_files)
print("Files with missing values:", files_with_missing)
print("Files with duplicate rows:", files_with_duplicates)

print("\n" + "=" * 60)
print("DATA QUALITY VALIDATION COMPLETED")
print("=" * 60)