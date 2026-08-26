# ============================================================
# CadetX Warehouse Analytics
# Week 04 — Warehouse Operations & Efficiency Analytics
# Step 02 — Warehouse Space Utilisation Analysis
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# 1. Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
FEATURES_DIR = DATA_DIR / "features"

INPUT_FILE = FEATURES_DIR / "warehouse_inventory_prepared.csv"
OUTPUT_FILE = FEATURES_DIR / "warehouse_space_utilisation.csv"


# ------------------------------------------------------------
# 2. Load Prepared Data
# ------------------------------------------------------------

print("=" * 70)
print("WEEK 04 — WAREHOUSE SPACE UTILISATION ANALYSIS")
print("=" * 70)

warehouse_inventory = pd.read_csv(INPUT_FILE)

print(
    f"\nPrepared dataset loaded: {warehouse_inventory.shape}"
)


# ------------------------------------------------------------
# 3. Warehouse-Level Aggregation
# ------------------------------------------------------------

warehouse_utilisation = (
    warehouse_inventory
    .groupby(
        [
            "branch_id",
            "branch_name",
            "city",
            "state",
            "region",
            "warehouse_type",
            "warehouse_capacity",
        ],
        dropna=False
    )
    .agg(
        total_products=("product_id", "nunique"),
        total_current_stock=("current_stock", "sum"),
        total_max_stock=("max_stock", "sum"),
        total_reorder_level=("reorder_level", "sum"),
        total_safety_stock=("safety_stock", "sum"),
    )
    .reset_index()
)


# ------------------------------------------------------------
# 4. Stock Utilisation
# ------------------------------------------------------------

warehouse_utilisation["stock_utilisation_pct"] = (
    warehouse_utilisation["total_current_stock"]
    / warehouse_utilisation["total_max_stock"]
) * 100


# ------------------------------------------------------------
# 5. Warehouse Capacity Utilisation
# ------------------------------------------------------------

warehouse_utilisation["capacity_utilisation_pct"] = (
    warehouse_utilisation["total_current_stock"]
    / warehouse_utilisation["warehouse_capacity"]
) * 100


# ------------------------------------------------------------
# 6. Available Capacity
# ------------------------------------------------------------

warehouse_utilisation["available_capacity"] = (
    warehouse_utilisation["warehouse_capacity"]
    - warehouse_utilisation["total_current_stock"]
)


# ------------------------------------------------------------
# 7. Utilisation Classification
# ------------------------------------------------------------

def classify_utilisation(value):

    if pd.isna(value):
        return "Unknown"

    if value < 50:
        return "Under-utilised"

    if value < 80:
        return "Moderately Utilised"

    if value <= 100:
        return "Highly Utilised"

    return "Capacity Pressure"


warehouse_utilisation["utilisation_status"] = (
    warehouse_utilisation["capacity_utilisation_pct"]
    .apply(classify_utilisation)
)


# ------------------------------------------------------------
# 8. Capacity Pressure Flag
# ------------------------------------------------------------

warehouse_utilisation["capacity_pressure_flag"] = (
    warehouse_utilisation["capacity_utilisation_pct"] > 100
)


# ------------------------------------------------------------
# 9. Round Values
# ------------------------------------------------------------

warehouse_utilisation[
    [
        "stock_utilisation_pct",
        "capacity_utilisation_pct",
    ]
] = warehouse_utilisation[
    [
        "stock_utilisation_pct",
        "capacity_utilisation_pct",
    ]
].round(2)


# ------------------------------------------------------------
# 10. Sort Warehouses
# ------------------------------------------------------------

warehouse_utilisation = (
    warehouse_utilisation
    .sort_values(
        "capacity_utilisation_pct",
        ascending=False
    )
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 11. Save Output
# ------------------------------------------------------------

warehouse_utilisation.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# 12. Summary
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("WAREHOUSE SPACE UTILISATION SUMMARY")
print("-" * 70)

print(
    "\nTotal warehouses analysed:",
    warehouse_utilisation["branch_id"].nunique()
)

print(
    "Average capacity utilisation:",
    round(
        warehouse_utilisation[
            "capacity_utilisation_pct"
        ].mean(),
        2
    ),
    "%"
)

print(
    "Highest capacity utilisation:",
    round(
        warehouse_utilisation[
            "capacity_utilisation_pct"
        ].max(),
        2
    ),
    "%"
)

print(
    "Warehouses under-utilised:",
    (
        warehouse_utilisation["utilisation_status"]
        == "Under-utilised"
    ).sum()
)

print(
    "Warehouses with capacity pressure:",
    warehouse_utilisation[
        "capacity_pressure_flag"
    ].sum()
)


# ------------------------------------------------------------
# 13. Display Results
# ------------------------------------------------------------

display_columns = [
    "branch_id",
    "branch_name",
    "warehouse_capacity",
    "total_current_stock",
    "capacity_utilisation_pct",
    "available_capacity",
    "utilisation_status",
]

print("\nWarehouse Utilisation Results:")

print(
    warehouse_utilisation[
        display_columns
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 14. Completion
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✓ Step 02 completed successfully.")
print(f"✓ Output saved to: {OUTPUT_FILE}")
print("=" * 70)