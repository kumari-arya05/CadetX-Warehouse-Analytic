import pandas as pd
from pathlib import Path

# Project data folder
DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Load all CSV files
csv_files = list(DATA_DIR.glob("*.csv"))

print("Total CSV files:", len(csv_files))

print("\nFiles found:")
for file in csv_files:
    print("-", file.name)

# Profile each dataset
print("\n" + "=" * 60)
print("DATA PROFILING")
print("=" * 60)

for file in csv_files:
    print(f"\n{'=' * 60}")
    print(f"FILE: {file.name}")
    print(f"{'=' * 60}")

    df = pd.read_csv(file)

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nColumn Names:")
    print(list(df.columns))

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:", df.duplicated().sum())

    print("\nFirst 5 Rows:")
    print(df.head())