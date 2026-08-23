import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

print("=" * 60)
print("MISSING VALUE ANALYSIS")
print("=" * 60)

file = CLEANED_DIR / "purchase_orders_header.csv"

df = pd.read_csv(file)

print("\nFile:", file.name)
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nMissing Values:")
print(df.isnull().sum()[df.isnull().sum() > 0])

print("\nDuplicate Rows:", df.duplicated().sum())

print("\nDecision:")
print("received_date missing values will be kept as blank.")
print("Reason: A missing received_date may indicate that the order")
print("has not yet been received.")

print("\n" + "=" * 60)
print("MISSING VALUE ANALYSIS COMPLETED")
print("=" * 60)