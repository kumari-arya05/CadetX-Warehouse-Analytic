# ============================================================
# CadetX Warehouse Analytics
# Week 04 — Warehouse Operations & Efficiency Analytics
# Step 05 — Product–Warehouse Alignment Analysis
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# 1. Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
FEATURES_DIR = DATA_DIR / "features"

INPUT_FILE = DATA_DIR / "inventory_master.csv"
OUTPUT_FILE = FEATURES_DIR / "product_warehouse_alignment.csv"


# ------------------------------------------------------------
# 2. Load Inventory Data
# ------------------------------------------------------------

print("=" * 70)
print("WEEK 04 — PRODUCT–WAREHOUSE ALIGNMENT ANALYSIS")
print("=" * 70)

inventory = pd.read_csv(INPUT_FILE)

print(
    f"\nInventory dataset loaded: {inventory.shape}"
)


# ------------------------------------------------------------
# 3. Standardise Column Names
# ------------------------------------------------------------

inventory.columns = (
    inventory.columns
    .str.strip()
    .str.lower()
)


# ------------------------------------------------------------
# 4. Validate Required Columns
# ------------------------------------------------------------

required_columns = [
    "product_id",
    "branch_id",
    "opening_stock",
    "reorder_level",
    "safety_stock",
    "max_stock",
    "current_stock",
    "warehouse_bin",
]

missing_columns = [
    column
    for column in required_columns
    if column not in inventory.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("✓ Required columns validated")


# ------------------------------------------------------------
# 5. Data Preparation
# ------------------------------------------------------------

numeric_columns = [
    "opening_stock",
    "reorder_level",
    "safety_stock",
    "max_stock",
    "current_stock",
]

for column in numeric_columns:
    inventory[column] = pd.to_numeric(
        inventory[column],
        errors="coerce"
    )


inventory["product_id"] = (
    inventory["product_id"]
    .astype("string")
    .str.strip()
)

inventory["branch_id"] = (
    inventory["branch_id"]
    .astype("string")
    .str.strip()
)

inventory["warehouse_bin"] = (
    inventory["warehouse_bin"]
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
    inventory.duplicated().sum()
)

print(
    "Missing product IDs:",
    inventory["product_id"].isna().sum()
)

print(
    "Missing branch IDs:",
    inventory["branch_id"].isna().sum()
)

print(
    "Missing warehouse bins:",
    inventory["warehouse_bin"].isna().sum()
)


# ------------------------------------------------------------
# 7. Product–Warehouse Mapping
# ------------------------------------------------------------

product_warehouse = (
    inventory
    .groupby(
        ["product_id", "branch_id"],
        dropna=False
    )
    .agg(
        warehouse_bins=("warehouse_bin", "nunique"),
        current_stock=("current_stock", "sum"),
        opening_stock=("opening_stock", "sum"),
        reorder_level=("reorder_level", "sum"),
        safety_stock=("safety_stock", "sum"),
        max_stock=("max_stock", "sum"),
    )
    .reset_index()
)


# ------------------------------------------------------------
# 8. Stock Allocation Percentage
# ------------------------------------------------------------

product_total_stock = (
    product_warehouse
    .groupby("product_id")["current_stock"]
    .transform("sum")
)

product_warehouse["stock_allocation_pct"] = (
    product_warehouse["current_stock"]
    / product_total_stock
) * 100

product_warehouse["stock_allocation_pct"] = (
    product_warehouse["stock_allocation_pct"]
    .replace([float("inf"), -float("inf")], pd.NA)
    .round(2)
)


# ------------------------------------------------------------
# 9. Warehouse Product Count
# ------------------------------------------------------------

warehouse_product_count = (
    product_warehouse
    .groupby("branch_id")["product_id"]
    .nunique()
    .rename("products_in_warehouse")
)

product_warehouse = product_warehouse.merge(
    warehouse_product_count,
    on="branch_id",
    how="left"
)


# ------------------------------------------------------------
# 10. Product Warehouse Count
# ------------------------------------------------------------

product_warehouse_count = (
    product_warehouse
    .groupby("product_id")["branch_id"]
    .nunique()
    .rename("warehouses_holding_product")
)

product_warehouse = product_warehouse.merge(
    product_warehouse_count,
    on="product_id",
    how="left"
)


# ------------------------------------------------------------
# 11. Stock Status
# ------------------------------------------------------------

def classify_stock(row):

    current = row["current_stock"]
    reorder = row["reorder_level"]
    safety = row["safety_stock"]
    maximum = row["max_stock"]

    if pd.isna(current):
        return "Unknown"

    if current <= safety:
        return "Critical"

    if current <= reorder:
        return "Low Stock"

    if current > maximum:
        return "Overstock"

    return "Healthy"


product_warehouse["stock_status"] = (
    product_warehouse.apply(
        classify_stock,
        axis=1
    )
)


# ------------------------------------------------------------
# 12. Alignment Classification
# ------------------------------------------------------------

def classify_alignment(row):

    warehouses = row["warehouses_holding_product"]
    allocation = row["stock_allocation_pct"]

    if pd.isna(warehouses) or pd.isna(allocation):
        return "Unknown"

    if warehouses == 1:
        return "Single-Warehouse"

    if warehouses >= 4:
        return "Highly Distributed"

    return "Multi-Warehouse"


product_warehouse["warehouse_alignment"] = (
    product_warehouse.apply(
        classify_alignment,
        axis=1
    )
)


# ------------------------------------------------------------
# 13. Sort Results
# ------------------------------------------------------------

product_warehouse = (
    product_warehouse
    .sort_values(
        [
            "product_id",
            "current_stock",
        ],
        ascending=[True, False]
    )
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 14. Save Output
# ------------------------------------------------------------

product_warehouse.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# 15. Summary
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("PRODUCT–WAREHOUSE ALIGNMENT SUMMARY")
print("-" * 70)

print(
    "\nUnique products:",
    product_warehouse["product_id"].nunique()
)

print(
    "Warehouses analysed:",
    product_warehouse["branch_id"].nunique()
)

print(
    "Product–warehouse combinations:",
    len(product_warehouse)
)

print("\nWarehouse Alignment:")
print(
    product_warehouse[
        "warehouse_alignment"
    ].value_counts()
)

print("\nStock Status:")
print(
    product_warehouse[
        "stock_status"
    ].value_counts()
)


# ------------------------------------------------------------
# 16. Display Results
# ------------------------------------------------------------

display_columns = [
    "product_id",
    "branch_id",
    "current_stock",
    "stock_allocation_pct",
    "warehouses_holding_product",
    "products_in_warehouse",
    "stock_status",
    "warehouse_alignment",
]

print("\nProduct–Warehouse Alignment Results:")

print(
    product_warehouse[
        display_columns
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 17. Completion
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✓ Step 05 completed successfully.")
print(f"✓ Output saved to: {OUTPUT_FILE}")
print("=" * 70)