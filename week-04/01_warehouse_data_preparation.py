# ============================================================
# CadetX Warehouse Analytics
# Week 04 — Warehouse Operations & Efficiency Analytics
# Step 01 — Warehouse Data Preparation
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# 1. Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "features"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load Source Datasets
# ------------------------------------------------------------

branches = pd.read_csv(DATA_DIR / "branches.csv")
inventory = pd.read_csv(DATA_DIR / "inventory_master.csv")
stock_ledger = pd.read_csv(DATA_DIR / "stock_ledger.csv")
sales_header = pd.read_csv(DATA_DIR / "sales_orders_header.csv")
sales_lines = pd.read_csv(DATA_DIR / "sales_orders_lines.csv")


print("=" * 70)
print("WEEK 04 — WAREHOUSE DATA PREPARATION")
print("=" * 70)

print("\nDataset Shapes:")
print(f"Branches       : {branches.shape}")
print(f"Inventory      : {inventory.shape}")
print(f"Stock Ledger   : {stock_ledger.shape}")
print(f"Sales Header   : {sales_header.shape}")
print(f"Sales Lines    : {sales_lines.shape}")


# ------------------------------------------------------------
# 3. Standardise Column Names
# ------------------------------------------------------------

datasets = {
    "branches": branches,
    "inventory": inventory,
    "stock_ledger": stock_ledger,
    "sales_header": sales_header,
    "sales_lines": sales_lines,
}

for name, df in datasets.items():
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )


# ------------------------------------------------------------
# 4. Duplicate Checks
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("DUPLICATE CHECK")
print("-" * 70)

for name, df in datasets.items():
    print(f"{name}: {df.duplicated().sum()} duplicate rows")


# ------------------------------------------------------------
# 5. Missing Value Checks
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("MISSING VALUE CHECK")
print("-" * 70)

for name, df in datasets.items():
    missing = df.isna().sum()
    missing = missing[missing > 0]

    print(f"\n{name}:")
    
    if missing.empty:
        print("No missing values found.")
    else:
        print(missing)


# ------------------------------------------------------------
# 6. Data Type Check
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("DATA TYPE CHECK")
print("-" * 70)

for name, df in datasets.items():
    print(f"\n{name}:")
    print(df.dtypes)


# ------------------------------------------------------------
# 7. Basic Referential Integrity Checks
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("REFERENTIAL INTEGRITY CHECK")
print("-" * 70)

branch_ids = set(branches["branch_id"].dropna())

inventory_branch_ids = set(
    inventory["branch_id"].dropna()
)

ledger_branch_ids = set(
    stock_ledger["branch_id"].dropna()
)

sales_branch_ids = set(
    sales_header["branch_id"].dropna()
)

print(
    "Inventory → Branches:",
    len(inventory_branch_ids - branch_ids),
    "unmatched branch IDs"
)

print(
    "Stock Ledger → Branches:",
    len(ledger_branch_ids - branch_ids),
    "unmatched branch IDs"
)

print(
    "Sales Header → Branches:",
    len(sales_branch_ids - branch_ids),
    "unmatched branch IDs"
)


# ------------------------------------------------------------
# 8. Numeric Conversion
# ------------------------------------------------------------

inventory_numeric = [
    "opening_stock",
    "reorder_level",
    "safety_stock",
    "max_stock",
    "current_stock",
]

for column in inventory_numeric:
    inventory[column] = pd.to_numeric(
        inventory[column],
        errors="coerce"
    )


if "quantity" in stock_ledger.columns:
    stock_ledger["quantity"] = pd.to_numeric(
        stock_ledger["quantity"],
        errors="coerce"
    )


if "warehouse_capacity" in branches.columns:
    branches["warehouse_capacity"] = pd.to_numeric(
        branches["warehouse_capacity"],
        errors="coerce"
    )


# ------------------------------------------------------------
# 9. Prepare Warehouse Inventory Dataset
# ------------------------------------------------------------

warehouse_inventory = inventory.merge(
    branches,
    on="branch_id",
    how="left",
    validate="many_to_one"
)


# ------------------------------------------------------------
# 10. Create Basic Warehouse Metrics
# ------------------------------------------------------------

warehouse_inventory["stock_utilisation_pct"] = (
    warehouse_inventory["current_stock"]
    / warehouse_inventory["max_stock"]
) * 100


warehouse_inventory["stock_vs_reorder"] = (
    warehouse_inventory["current_stock"]
    - warehouse_inventory["reorder_level"]
)


warehouse_inventory["stock_vs_safety"] = (
    warehouse_inventory["current_stock"]
    - warehouse_inventory["safety_stock"]
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


warehouse_inventory["stock_status"] = (
    warehouse_inventory.apply(
        classify_stock,
        axis=1
    )
)


# ------------------------------------------------------------
# 12. Save Prepared Dataset
# ------------------------------------------------------------

output_file = (
    OUTPUT_DIR
    / "warehouse_inventory_prepared.csv"
)

warehouse_inventory.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# 13. Final Summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATA PREPARATION COMPLETED")
print("=" * 70)

print(
    f"\nPrepared dataset saved to:\n{output_file}"
)

print(
    f"\nPrepared dataset shape: "
    f"{warehouse_inventory.shape}"
)

print("\nStock Status:")
print(
    warehouse_inventory["stock_status"]
    .value_counts()
)

print("\n✓ Step 01 completed successfully.")