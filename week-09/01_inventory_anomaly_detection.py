import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# WEEK 09 - INVENTORY MOVEMENT ANOMALY DETECTION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "week-09" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def find_csv(filename):
    """Find a CSV file anywhere inside the project."""
    matches = list(BASE_DIR.rglob(filename))
    if matches:
        return matches[0]
    return None


# ------------------------------------------------------------
# 1. Load stock ledger
# ------------------------------------------------------------

stock_file = find_csv("stock_ledger.csv")

if stock_file is None:
    print("ERROR: stock_ledger.csv not found.")
    print("Please make sure the dataset is available in the project.")
    raise SystemExit(1)

df = pd.read_csv(stock_file)

print("=" * 60)
print("WEEK 09 - INVENTORY MOVEMENT ANOMALY DETECTION")
print("=" * 60)

print(f"\nDataset: {stock_file}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print("\nAvailable columns:")
print(list(df.columns))


# ------------------------------------------------------------
# 2. Detect numeric quantity column
# ------------------------------------------------------------

quantity_candidates = [
    "quantity",
    "qty",
    "movement_quantity",
    "transaction_quantity",
    "stock_quantity",
    "units",
    "units_moved"
]

quantity_col = None

for col in quantity_candidates:
    if col in df.columns:
        quantity_col = col
        break

if quantity_col is None:
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:
        quantity_col = numeric_cols[-1]

if quantity_col is None:
    print("\nERROR: No numeric quantity column found.")
    raise SystemExit(1)

print(f"\nQuantity column selected: {quantity_col}")


# ------------------------------------------------------------
# 3. Convert quantity to numeric
# ------------------------------------------------------------

df[quantity_col] = pd.to_numeric(
    df[quantity_col],
    errors="coerce"
)

df = df.dropna(subset=[quantity_col]).copy()


# ------------------------------------------------------------
# 4. Calculate anomaly thresholds
# ------------------------------------------------------------

Q1 = df[quantity_col].quantile(0.25)
Q3 = df[quantity_col].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - (1.5 * IQR)
upper_limit = Q3 + (1.5 * IQR)


# ------------------------------------------------------------
# 5. Detect anomalies
# ------------------------------------------------------------

df["anomaly_flag"] = np.where(
    (df[quantity_col] < lower_limit) |
    (df[quantity_col] > upper_limit),
    "Anomaly",
    "Normal"
)

df["anomaly_reason"] = np.where(
    df[quantity_col] > upper_limit,
    "Unusually high inventory movement",
    np.where(
        df[quantity_col] < lower_limit,
        "Unusually low inventory movement",
        "Within normal range"
    )
)


# ------------------------------------------------------------
# 6. Add anomaly score
# ------------------------------------------------------------

median = df[quantity_col].median()
std = df[quantity_col].std()

if std == 0 or pd.isna(std):
    df["anomaly_score"] = 0
else:
    df["anomaly_score"] = (
        (df[quantity_col] - median).abs() / std
    ).round(2)


# ------------------------------------------------------------
# 7. Sort anomalies first
# ------------------------------------------------------------

df["anomaly_priority"] = np.where(
    df["anomaly_flag"] == "Anomaly",
    1,
    0
)

df = df.sort_values(
    ["anomaly_priority", "anomaly_score"],
    ascending=[False, False]
)

df = df.drop(columns=["anomaly_priority"])


# ------------------------------------------------------------
# 8. Save complete analysis
# ------------------------------------------------------------

output_file = OUTPUT_DIR / "inventory_movement_anomalies.csv"

df.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# 9. Summary
# ------------------------------------------------------------

total_records = len(df)
anomaly_count = (df["anomaly_flag"] == "Anomaly").sum()
normal_count = (df["anomaly_flag"] == "Normal").sum()

anomaly_percentage = (
    anomaly_count / total_records * 100
    if total_records > 0
    else 0
)

print("\n" + "=" * 60)
print("ANALYSIS SUMMARY")
print("=" * 60)

print(f"Total records       : {total_records:,}")
print(f"Normal records      : {normal_count:,}")
print(f"Anomalous records   : {anomaly_count:,}")
print(f"Anomaly percentage   : {anomaly_percentage:.2f}%")

print(f"\nLower threshold     : {lower_limit:.2f}")
print(f"Upper threshold     : {upper_limit:.2f}")

print(f"\nOutput saved to:")
print(output_file)

print("\nWeek 09 anomaly detection completed successfully.")