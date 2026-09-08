import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# WEEK 09 - STOCK SHRINKAGE DETECTION
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
print("WEEK 09 - STOCK SHRINKAGE DETECTION")
print("=" * 60)

print(f"\nDataset: {stock_file}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print("\nAvailable columns:")
print(list(df.columns))


# ------------------------------------------------------------
# 2. Identify stock quantity column
# ------------------------------------------------------------

quantity_candidates = [
    "quantity",
    "qty",
    "stock_quantity",
    "closing_stock",
    "closing_quantity",
    "balance_quantity",
    "stock_balance",
    "units"
]

quantity_col = None

for col in quantity_candidates:
    if col in df.columns:
        quantity_col = col
        break


# If standard column is not found, use numeric column
if quantity_col is None:
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:
        quantity_col = numeric_cols[-1]


if quantity_col is None:
    print("\nERROR: No numeric stock quantity column found.")
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
# 4. Detect negative stock / unusual stock values
# ------------------------------------------------------------

df["shrinkage_flag"] = "Normal"
df["shrinkage_reason"] = "No shrinkage indicator detected"


# Negative stock is a direct control exception
negative_stock = df[quantity_col] < 0

df.loc[negative_stock, "shrinkage_flag"] = "Potential Shrinkage"
df.loc[
    negative_stock,
    "shrinkage_reason"
] = "Negative stock balance detected"


# ------------------------------------------------------------
# 5. Statistical shrinkage detection
# ------------------------------------------------------------

Q1 = df[quantity_col].quantile(0.25)
Q3 = df[quantity_col].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - (1.5 * IQR)

# Only apply statistical detection when the lower
# threshold is positive.
if lower_limit > 0:

    unusual_low_stock = (
        (df[quantity_col] < lower_limit) &
        (df[quantity_col] >= 0)
    )

    df.loc[
        unusual_low_stock,
        "shrinkage_flag"
    ] = "Potential Shrinkage"

    df.loc[
        unusual_low_stock,
        "shrinkage_reason"
    ] = "Unusually low stock level"


# ------------------------------------------------------------
# 6. Calculate shrinkage risk score
# ------------------------------------------------------------

median_stock = df[quantity_col].median()
std_stock = df[quantity_col].std()

if std_stock == 0 or pd.isna(std_stock):
    df["shrinkage_risk_score"] = 0
else:
    df["shrinkage_risk_score"] = (
        (median_stock - df[quantity_col]) / std_stock
    ).clip(lower=0).round(2)


# ------------------------------------------------------------
# 7. Risk classification
# ------------------------------------------------------------

def classify_risk(row):

    if row["shrinkage_flag"] == "Potential Shrinkage":

        score = row["shrinkage_risk_score"]

        if row[quantity_col] < 0:
            return "High"

        if score >= 2:
            return "High"

        if score >= 1:
            return "Medium"

        return "Low"

    return "None"


df["shrinkage_risk"] = df.apply(
    classify_risk,
    axis=1
)


# ------------------------------------------------------------
# 8. Sort potential shrinkage cases first
# ------------------------------------------------------------

risk_order = {
    "High": 3,
    "Medium": 2,
    "Low": 1,
    "None": 0
}

df["_risk_order"] = df["shrinkage_risk"].map(risk_order)

df = df.sort_values(
    ["_risk_order", "shrinkage_risk_score"],
    ascending=[False, False]
)

df = df.drop(columns=["_risk_order"])


# ------------------------------------------------------------
# 9. Save output
# ------------------------------------------------------------

output_file = OUTPUT_DIR / "stock_shrinkage_analysis.csv"

df.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# 10. Summary
# ------------------------------------------------------------

total_records = len(df)

shrinkage_records = (
    df["shrinkage_flag"] == "Potential Shrinkage"
).sum()

high_risk = (
    df["shrinkage_risk"] == "High"
).sum()

medium_risk = (
    df["shrinkage_risk"] == "Medium"
).sum()

low_risk = (
    df["shrinkage_risk"] == "Low"
).sum()


print("\n" + "=" * 60)
print("STOCK SHRINKAGE ANALYSIS SUMMARY")
print("=" * 60)

print(f"Total records          : {total_records:,}")
print(f"Potential shrinkage    : {shrinkage_records:,}")
print(f"High-risk cases        : {high_risk:,}")
print(f"Medium-risk cases      : {medium_risk:,}")
print(f"Low-risk cases         : {low_risk:,}")

print(f"\nLower threshold        : {lower_limit:.2f}")

print("\nOutput saved to:")
print(output_file)

print("\nWeek 09 stock shrinkage detection completed successfully.")