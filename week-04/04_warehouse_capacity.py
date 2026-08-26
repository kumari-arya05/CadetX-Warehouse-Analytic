# ============================================================
# CadetX Warehouse Analytics
# Week 04 — Warehouse Operations & Efficiency Analytics
# Step 04 — Warehouse Capacity Analysis
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# 1. Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
FEATURES_DIR = DATA_DIR / "features"

INPUT_FILE = FEATURES_DIR / "warehouse_space_utilisation.csv"
OUTPUT_FILE = FEATURES_DIR / "warehouse_capacity_analysis.csv"


# ------------------------------------------------------------
# 2. Load Space Utilisation Data
# ------------------------------------------------------------

print("=" * 70)
print("WEEK 04 — WAREHOUSE CAPACITY ANALYSIS")
print("=" * 70)

warehouse = pd.read_csv(INPUT_FILE)

print(
    f"\nSpace utilisation dataset loaded: {warehouse.shape}"
)


# ------------------------------------------------------------
# 3. Validate Required Columns
# ------------------------------------------------------------

required_columns = [
    "branch_id",
    "branch_name",
    "warehouse_capacity",
    "total_current_stock",
    "total_max_stock",
    "total_reorder_level",
    "total_safety_stock",
    "capacity_utilisation_pct",
]

missing_columns = [
    column
    for column in required_columns
    if column not in warehouse.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("✓ Required columns validated")


# ------------------------------------------------------------
# 4. Numeric Conversion
# ------------------------------------------------------------

numeric_columns = [
    "warehouse_capacity",
    "total_current_stock",
    "total_max_stock",
    "total_reorder_level",
    "total_safety_stock",
    "capacity_utilisation_pct",
]

for column in numeric_columns:
    warehouse[column] = pd.to_numeric(
        warehouse[column],
        errors="coerce"
    )


# ------------------------------------------------------------
# 5. Calculate Remaining Capacity
# ------------------------------------------------------------

warehouse["remaining_capacity"] = (
    warehouse["warehouse_capacity"]
    - warehouse["total_current_stock"]
)


# ------------------------------------------------------------
# 6. Calculate Capacity Gap
# ------------------------------------------------------------

warehouse["capacity_gap_pct"] = (
    100
    - warehouse["capacity_utilisation_pct"]
)


# ------------------------------------------------------------
# 7. Calculate Stock Headroom
# ------------------------------------------------------------

warehouse["stock_headroom"] = (
    warehouse["total_max_stock"]
    - warehouse["total_current_stock"]
)


# ------------------------------------------------------------
# 8. Capacity Status
# ------------------------------------------------------------

def classify_capacity(utilisation):

    if pd.isna(utilisation):
        return "Unknown"

    if utilisation > 100:
        return "Over Capacity"

    if utilisation >= 80:
        return "High Capacity Usage"

    if utilisation >= 50:
        return "Moderate Capacity Usage"

    return "Low Capacity Usage"


warehouse["capacity_status"] = (
    warehouse["capacity_utilisation_pct"]
    .apply(classify_capacity)
)


# ------------------------------------------------------------
# 9. Capacity Pressure Flag
# ------------------------------------------------------------

warehouse["capacity_pressure"] = (
    warehouse["capacity_utilisation_pct"] > 100
)


# ------------------------------------------------------------
# 10. Capacity Risk Level
# ------------------------------------------------------------

def classify_capacity_risk(utilisation):

    if pd.isna(utilisation):
        return "Unknown"

    if utilisation > 100:
        return "Critical"

    if utilisation >= 90:
        return "High"

    if utilisation >= 80:
        return "Moderate"

    return "Low"


warehouse["capacity_risk_level"] = (
    warehouse["capacity_utilisation_pct"]
    .apply(classify_capacity_risk)
)


# ------------------------------------------------------------
# 11. Round Analytical Values
# ------------------------------------------------------------

round_columns = [
    "capacity_utilisation_pct",
    "capacity_gap_pct",
]

warehouse[round_columns] = (
    warehouse[round_columns].round(2)
)


# ------------------------------------------------------------
# 12. Sort by Capacity Utilisation
# ------------------------------------------------------------

warehouse = (
    warehouse
    .sort_values(
        "capacity_utilisation_pct",
        ascending=False
    )
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 13. Add Capacity Usage Rank
# ------------------------------------------------------------

warehouse["capacity_usage_rank"] = (
    warehouse["capacity_utilisation_pct"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype("Int64")
)


# ------------------------------------------------------------
# 14. Save Output
# ------------------------------------------------------------

warehouse.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# 15. Summary
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("WAREHOUSE CAPACITY SUMMARY")
print("-" * 70)

print(
    "\nWarehouses analysed:",
    warehouse["branch_id"].nunique()
)

print(
    "Average capacity utilisation:",
    round(
        warehouse[
            "capacity_utilisation_pct"
        ].mean(),
        2
    ),
    "%"
)

print(
    "Maximum capacity utilisation:",
    round(
        warehouse[
            "capacity_utilisation_pct"
        ].max(),
        2
    ),
    "%"
)

print(
    "Warehouses over capacity:",
    warehouse[
        "capacity_pressure"
    ].sum()
)

print("\nCapacity Status:")
print(
    warehouse[
        "capacity_status"
    ].value_counts()
)

print("\nCapacity Risk Level:")
print(
    warehouse[
        "capacity_risk_level"
    ].value_counts()
)


# ------------------------------------------------------------
# 16. Display Results
# ------------------------------------------------------------

display_columns = [
    "branch_id",
    "branch_name",
    "warehouse_capacity",
    "total_current_stock",
    "remaining_capacity",
    "capacity_utilisation_pct",
    "capacity_status",
    "capacity_risk_level",
]

print("\nWarehouse Capacity Results:")

print(
    warehouse[
        display_columns
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 17. Completion
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✓ Step 04 completed successfully.")
print(f"✓ Output saved to: {OUTPUT_FILE}")
print("=" * 70)