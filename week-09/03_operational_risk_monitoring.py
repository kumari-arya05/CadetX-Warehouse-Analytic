import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# WEEK 09 - OPERATIONAL RISK MONITORING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "week-09" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def find_csv(filename):
    matches = list(BASE_DIR.rglob(filename))
    if matches:
        return matches[0]
    return None


# ------------------------------------------------------------
# 1. Load Stock Ledger
# ------------------------------------------------------------

stock_file = find_csv("stock_ledger.csv")

if stock_file is None:
    print("ERROR: stock_ledger.csv not found.")
    raise SystemExit(1)

df = pd.read_csv(stock_file)

print("=" * 60)
print("WEEK 09 - OPERATIONAL RISK MONITORING")
print("=" * 60)

print(f"\nDataset: {stock_file}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# ------------------------------------------------------------
# 2. Identify important columns
# ------------------------------------------------------------

quantity_candidates = [
    "quantity",
    "qty",
    "movement_quantity",
    "transaction_quantity",
    "stock_quantity",
    "units"
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
    print("ERROR: Quantity column not found.")
    raise SystemExit(1)

df[quantity_col] = pd.to_numeric(
    df[quantity_col],
    errors="coerce"
)

df = df.dropna(subset=[quantity_col]).copy()


# ------------------------------------------------------------
# 3. Risk indicators
# ------------------------------------------------------------

df["negative_stock_risk"] = np.where(
    df[quantity_col] < 0,
    "High",
    "None"
)


# Extremely large movements
Q1 = df[quantity_col].quantile(0.25)
Q3 = df[quantity_col].quantile(0.75)
IQR = Q3 - Q1

upper_limit = Q3 + (1.5 * IQR)

df["unusual_movement_risk"] = np.where(
    df[quantity_col].abs() > abs(upper_limit),
    "High",
    "None"
)


# Very low / zero stock risk
df["low_stock_risk"] = np.where(
    df[quantity_col] <= 0,
    "High",
    "None"
)


# ------------------------------------------------------------
# 4. Overall operational risk
# ------------------------------------------------------------

def calculate_risk(row):

    risks = [
        row["negative_stock_risk"],
        row["unusual_movement_risk"],
        row["low_stock_risk"]
    ]

    if "High" in risks:
        return "High"

    return "Low"


df["operational_risk"] = df.apply(
    calculate_risk,
    axis=1
)


# ------------------------------------------------------------
# 5. Risk reason
# ------------------------------------------------------------

def risk_reason(row):

    reasons = []

    if row["negative_stock_risk"] == "High":
        reasons.append("Negative stock")

    if row["unusual_movement_risk"] == "High":
        reasons.append("Unusual movement")

    if row["low_stock_risk"] == "High":
        reasons.append("Low/zero stock")

    if not reasons:
        return "No major operational risk detected"

    return "; ".join(reasons)


df["risk_reason"] = df.apply(
    risk_reason,
    axis=1
)


# ------------------------------------------------------------
# 6. Risk score
# ------------------------------------------------------------

df["risk_score"] = np.where(
    df["operational_risk"] == "High",
    2,
    0
)


# ------------------------------------------------------------
# 7. Sort high-risk records first
# ------------------------------------------------------------

df = df.sort_values(
    ["risk_score", quantity_col],
    ascending=[False, True]
)


# ------------------------------------------------------------
# 8. Save operational risk analysis
# ------------------------------------------------------------

output_file = OUTPUT_DIR / "operational_risk_monitoring.csv"

df.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# 9. Summary
# ------------------------------------------------------------

total_records = len(df)

high_risk = (
    df["operational_risk"] == "High"
).sum()

low_risk = (
    df["operational_risk"] == "Low"
).sum()

risk_percentage = (
    high_risk / total_records * 100
    if total_records > 0
    else 0
)


print("\n" + "=" * 60)
print("OPERATIONAL RISK SUMMARY")
print("=" * 60)

print(f"Total records       : {total_records:,}")
print(f"High-risk records   : {high_risk:,}")
print(f"Low-risk records    : {low_risk:,}")
print(f"Risk percentage     : {risk_percentage:.2f}%")

print(f"\nOutput saved to:")
print(output_file)

print("\nWeek 09 operational risk monitoring completed successfully.")