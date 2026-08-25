import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# WEEK 03 - FEATURE ENGINEERING FOR ANALYTICS
# ============================================================

print("=" * 70)
print("WEEK 03 - FEATURE ENGINEERING")
print("=" * 70)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
INTEGRATED_DIR = DATA_DIR / "integrated"

FEATURE_DIR = DATA_DIR / "features"

FEATURE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"Project root: {PROJECT_ROOT}")
print(f"Integrated data folder: {INTEGRATED_DIR}")
print(f"Feature output folder: {FEATURE_DIR}")


# ============================================================
# 2. LOAD INTEGRATED MASTER DATA
# ============================================================

master_file = (
    INTEGRATED_DIR /
    "product_inventory_sales_master.csv"
)


if not master_file.exists():
    raise FileNotFoundError(
        f"Integrated master file not found: {master_file}"
    )


df = pd.read_csv(master_file)


print()
print("Integrated master dataset loaded successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# 3. STANDARDIZE COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
)


# ============================================================
# 4. NUMERIC FEATURE CONVERSION
# ============================================================

numeric_candidates = [
    "current_stock",
    "safety_stock",
    "reorder_level",
    "max_stock",
    "unit_cost",
    "unit_price",
    "quantity",
    "total_quantity_sold",
    "total_sales_value",
    "line_grand_total"
]


for column in numeric_candidates:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# 5. SALES & INVENTORY FEATURES
# ============================================================

if (
    "total_quantity_sold" in df.columns
    and "current_stock" in df.columns
):

    df["stock_to_sales_ratio"] = np.where(
        df["total_quantity_sold"] > 0,
        df["current_stock"] /
        df["total_quantity_sold"],
        np.nan
    )


if (
    "total_sales_value" in df.columns
    and "total_quantity_sold" in df.columns
):

    df["average_selling_price"] = np.where(
        df["total_quantity_sold"] > 0,
        df["total_sales_value"] /
        df["total_quantity_sold"],
        np.nan
    )


# ============================================================
# 6. STOCK POSITION FEATURES
# ============================================================

if (
    "current_stock" in df.columns
    and "reorder_level" in df.columns
):

    df["stock_above_reorder"] = (
        df["current_stock"] -
        df["reorder_level"]
    )


if (
    "current_stock" in df.columns
    and "max_stock" in df.columns
):

    df["stock_to_max_ratio"] = np.where(
        df["max_stock"] > 0,
        df["current_stock"] /
        df["max_stock"],
        np.nan
    )


if (
    "current_stock" in df.columns
    and "safety_stock" in df.columns
):

    df["stock_above_safety"] = (
        df["current_stock"] -
        df["safety_stock"]
    )


# ============================================================
# 7. PRODUCT MARGIN FEATURES
# ============================================================

if (
    "unit_price" in df.columns
    and "unit_cost" in df.columns
):

    df["unit_margin"] = (
        df["unit_price"] -
        df["unit_cost"]
    )


    df["margin_percentage"] = np.where(
        df["unit_price"] > 0,
        (
            (
                df["unit_price"] -
                df["unit_cost"]
            )
            /
            df["unit_price"]
        ) * 100,
        np.nan
    )


# ============================================================
# 8. ESTIMATED INVENTORY VALUE
# ============================================================

if (
    "current_stock" in df.columns
    and "unit_cost" in df.columns
):

    df["inventory_cost_value"] = (
        df["current_stock"] *
        df["unit_cost"]
    )


if (
    "current_stock" in df.columns
    and "unit_price" in df.columns
):

    df["inventory_retail_value"] = (
        df["current_stock"] *
        df["unit_price"]
    )


# ============================================================
# 9. DEMAND / MOVEMENT FEATURES
# ============================================================

if "total_quantity_sold" in df.columns:

    df["demand_level"] = pd.cut(
        df["total_quantity_sold"],
        bins=[
            -np.inf,
            0,
            df["total_quantity_sold"].quantile(0.50),
            df["total_quantity_sold"].quantile(0.75),
            np.inf
        ],
        labels=[
            "No Demand",
            "Low Demand",
            "Medium Demand",
            "High Demand"
        ],
        duplicates="drop"
    )


# ============================================================
# 10. INVENTORY RISK FEATURES
# ============================================================

if (
    "current_stock" in df.columns
    and "reorder_level" in df.columns
):

    df["reorder_risk_flag"] = np.where(
        df["current_stock"] <
        df["reorder_level"],
        "At Risk",
        "Normal"
    )


if (
    "current_stock" in df.columns
    and "max_stock" in df.columns
):

    df["overstock_flag"] = np.where(
        df["current_stock"] >
        df["max_stock"],
        "Overstock",
        "Normal"
    )


# ============================================================
# 11. DATE FEATURES
# ============================================================

date_columns = [
    column
    for column in df.columns
    if "date" in column
]


for column in date_columns:

    df[column] = pd.to_datetime(
        df[column],
        errors="coerce"
    )


    df[f"{column}_year"] = (
        df[column].dt.year
    )

    df[f"{column}_month"] = (
        df[column].dt.month
    )

    df[f"{column}_month_name"] = (
        df[column].dt.month_name()
    )

    df[f"{column}_quarter"] = (
        df[column].dt.quarter
    )


# ============================================================
# 12. DATA COMPLETENESS FEATURES
# ============================================================

df["missing_value_count"] = (
    df.isna().sum(axis=1)
)


df["data_completeness_percentage"] = (
    (
        1 -
        (
            df.isna().sum(axis=1) /
            len(df.columns)
        )
    )
    * 100
)


# ============================================================
# 13. FEATURE ENGINEERING SUMMARY
# ============================================================

feature_columns = [
    column
    for column in df.columns
    if column not in pd.read_csv(master_file, nrows=0).columns
]


feature_summary = pd.DataFrame(
    {
        "feature_name": feature_columns,
        "data_type": [
            str(df[column].dtype)
            for column in feature_columns
        ],
        "missing_values": [
            int(df[column].isna().sum())
            for column in feature_columns
        ]
    }
)


# ============================================================
# 14. SAVE FEATURE-ENGINEERED DATA
# ============================================================

feature_output_file = (
    FEATURE_DIR /
    "product_inventory_sales_features.csv"
)


df.to_csv(
    feature_output_file,
    index=False
)


# ============================================================
# 15. SAVE FEATURE SUMMARY
# ============================================================

feature_summary_file = (
    FEATURE_DIR /
    "feature_engineering_summary.csv"
)


feature_summary.to_csv(
    feature_summary_file,
    index=False
)


# ============================================================
# 16. FINAL STATUS
# ============================================================

print()
print("=" * 70)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 70)

print(
    f"Original features: "
    f"{len(df.columns) - len(feature_columns)}"
)

print(
    f"New engineered features: "
    f"{len(feature_columns)}"
)

print(
    f"Final columns: "
    f"{len(df.columns)}"
)

print()
print(
    f"Feature dataset saved: "
    f"{feature_output_file}"
)

print(
    f"Feature summary saved: "
    f"{feature_summary_file}"
)

print()
print("All feature engineering outputs generated successfully.")