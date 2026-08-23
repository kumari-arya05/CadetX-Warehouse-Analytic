import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

# Create cleaned-data folder
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("DATA CLEANING")
print("=" * 60)

# Process every CSV file
csv_files = list(DATA_DIR.glob("*.csv"))

for file in csv_files:

    # Skip files already inside cleaned folder
    if file.parent == CLEANED_DIR:
        continue

    print(f"\nProcessing: {file.name}")

    df = pd.read_csv(file)

    # Remove completely empty rows
    before_rows = len(df)
    df = df.dropna(how="all")
    removed_empty_rows = before_rows - len(df)

    # Remove duplicate rows
    before_duplicates = len(df)
    df = df.drop_duplicates()
    removed_duplicates = before_duplicates - len(df)

    # Remove extra spaces from text columns
    text_columns = df.select_dtypes(include=["object"]).columns

    for column in text_columns:
        df[column] = df[column].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    # Save cleaned dataset
    output_file = CLEANED_DIR / file.name
    df.to_csv(output_file, index=False)

    print("Original rows:", before_rows)
    print("Empty rows removed:", removed_empty_rows)
    print("Duplicate rows removed:", removed_duplicates)
    print("Final rows:", len(df))
    print("Saved to:", output_file)

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)