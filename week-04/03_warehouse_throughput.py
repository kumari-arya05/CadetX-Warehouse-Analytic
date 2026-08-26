# ============================================================
# CadetX Warehouse Analytics
# Week 04 — Warehouse Operations & Efficiency Analytics
# Step 03 — Warehouse Throughput Analysis
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# 1. Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
FEATURES_DIR = DATA_DIR / "features"

INPUT_FILE = DATA_DIR / "stock_ledger.csv"
OUTPUT_FILE = FEATURES_DIR / "warehouse_throughput.csv"


# ------------------------------------------------------------
# 2. Load Stock Ledger
# ------------------------------------------------------------

print("=" * 70)
print("WEEK 04 — WAREHOUSE THROUGHPUT ANALYSIS")
print("=" * 70)

stock_ledger = pd.read_csv(INPUT_FILE)

print(
    f"\nStock ledger loaded: {stock_ledger.shape}"
)


# ------------------------------------------------------------
# 3. Standardise Columns
# ------------------------------------------------------------

stock_ledger.columns = (
    stock_ledger.columns
    .str.strip()
    .str.lower()
)


# ------------------------------------------------------------
# 4. Validate Required Columns
# ------------------------------------------------------------

required_columns = [
    "movement_id",
    "product_id",
    "branch_id",
    "movement_type",
    "movement_date",
    "quantity",
    "reference_type",
    "reference_id",
    "running_balance",
]

missing_columns = [
    column
    for column in required_columns
    if column not in stock_ledger.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("✓ Required columns validated")


# ------------------------------------------------------------
# 5. Data Preparation
# ------------------------------------------------------------

stock_ledger["quantity"] = pd.to_numeric(
    stock_ledger["quantity"],
    errors="coerce"
)

stock_ledger["running_balance"] = pd.to_numeric(
    stock_ledger["running_balance"],
    errors="coerce"
)

stock_ledger["movement_date"] = pd.to_datetime(
    stock_ledger["movement_date"],
    errors="coerce"
)

stock_ledger["movement_type"] = (
    stock_ledger["movement_type"]
    .astype("string")
    .str.strip()
    .str.upper()
)

stock_ledger["branch_id"] = (
    stock_ledger["branch_id"]
    .astype("string")
    .str.strip()
)


# ------------------------------------------------------------
# 6. Basic Quality Checks
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("DATA QUALITY CHECK")
print("-" * 70)

print(
    "Duplicate rows:",
    stock_ledger.duplicated().sum()
)

print(
    "Missing movement dates:",
    stock_ledger["movement_date"].isna().sum()
)

print(
    "Missing quantities:",
    stock_ledger["quantity"].isna().sum()
)

print("\nMovement Types:")
print(
    stock_ledger["movement_type"]
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 7. Movement Direction
# ------------------------------------------------------------

stock_ledger["inbound_quantity"] = stock_ledger["quantity"].where(
    stock_ledger["movement_type"] == "IN",
    0
)

stock_ledger["outbound_quantity"] = stock_ledger["quantity"].where(
    stock_ledger["movement_type"] == "OUT",
    0
)

stock_ledger["adjustment_quantity"] = stock_ledger["quantity"].where(
    stock_ledger["movement_type"] == "ADJUSTMENT",
    0
)


# ------------------------------------------------------------
# 8. Warehouse-Level Throughput
# ------------------------------------------------------------

warehouse_throughput = (
    stock_ledger
    .groupby(
        "branch_id",
        dropna=False
    )
    .agg(
        total_movements=("movement_id", "nunique"),
        total_inbound_quantity=("inbound_quantity", "sum"),
        total_outbound_quantity=("outbound_quantity", "sum"),
        total_adjustment_quantity=("adjustment_quantity", "sum"),
        total_movement_quantity=("quantity", "sum"),
        unique_products_moved=("product_id", "nunique"),
    )
    .reset_index()
)


# ------------------------------------------------------------
# 9. Calculate Throughput
# ------------------------------------------------------------

warehouse_throughput["total_throughput"] = (
    warehouse_throughput["total_inbound_quantity"]
    + warehouse_throughput["total_outbound_quantity"]
)


# ------------------------------------------------------------
# 10. Net Stock Movement
# ------------------------------------------------------------

warehouse_throughput["net_stock_movement"] = (
    warehouse_throughput["total_inbound_quantity"]
    - warehouse_throughput["total_outbound_quantity"]
)


# ------------------------------------------------------------
# 11. Movement Activity Ratio
# ------------------------------------------------------------

warehouse_throughput["outbound_to_inbound_ratio"] = (
    warehouse_throughput["total_outbound_quantity"]
    / warehouse_throughput["total_inbound_quantity"]
)

warehouse_throughput["outbound_to_inbound_ratio"] = (
    warehouse_throughput[
        "outbound_to_inbound_ratio"
    ]
    .replace([float("inf"), -float("inf")], pd.NA)
    .round(2)
)


# ------------------------------------------------------------
# 12. Sort Warehouses by Throughput
# ------------------------------------------------------------

warehouse_throughput = (
    warehouse_throughput
    .sort_values(
        "total_throughput",
        ascending=False
    )
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 13. Add Throughput Ranking
# ------------------------------------------------------------

warehouse_throughput["throughput_rank"] = (
    warehouse_throughput[
        "total_throughput"
    ]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)


# ------------------------------------------------------------
# 14. Save Output
# ------------------------------------------------------------

warehouse_throughput.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# 15. Summary
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("WAREHOUSE THROUGHPUT SUMMARY")
print("-" * 70)

print(
    "\nWarehouses analysed:",
    warehouse_throughput["branch_id"].nunique()
)

print(
    "Total movements:",
    warehouse_throughput["total_movements"].sum()
)

print(
    "Total inbound quantity:",
    warehouse_throughput[
        "total_inbound_quantity"
    ].sum()
)

print(
    "Total outbound quantity:",
    warehouse_throughput[
        "total_outbound_quantity"
    ].sum()
)

print(
    "Total throughput:",
    warehouse_throughput[
        "total_throughput"
    ].sum()
)


# ------------------------------------------------------------
# 16. Display Results
# ------------------------------------------------------------

display_columns = [
    "branch_id",
    "total_movements",
    "total_inbound_quantity",
    "total_outbound_quantity",
    "total_adjustment_quantity",
    "total_throughput",
    "unique_products_moved",
    "outbound_to_inbound_ratio",
    "throughput_rank",
]

print("\nWarehouse Throughput Results:")

print(
    warehouse_throughput[
        display_columns
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 17. Completion
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✓ Step 03 completed successfully.")
print(f"✓ Output saved to: {OUTPUT_FILE}")
print("=" * 70)