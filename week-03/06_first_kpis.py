import pandas as pd
from pathlib import Path


# ============================================================
# WEEK 03 - FIRST KPIs
# ============================================================

print("=" * 70)
print("WEEK 03 - FIRST KPI ANALYSIS")
print("=" * 70)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
FEATURE_DIR = DATA_DIR / "features"
KPI_DIR = DATA_DIR / "kpis"

KPI_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"Project root: {PROJECT_ROOT}")
print(f"KPI output folder: {KPI_DIR}")


# ============================================================
# 2. FEATURE DATASET
# ============================================================

FEATURE_FILE = (
    FEATURE_DIR /
    "product_inventory_sales_features.csv"
)


if not FEATURE_FILE.exists():

    raise FileNotFoundError(
        f"Feature dataset not found: {FEATURE_FILE}"
    )


df = pd.read_csv(FEATURE_FILE)


print()
print(f"Feature dataset loaded: {df.shape}")


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
# 4. HELPER FUNCTIONS
# ============================================================

def first_existing(columns):
    for column in columns:
        if column in df.columns:
            return column
    return None


def numeric_sum(column):
    if column is None:
        return 0
    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0).sum()


# ============================================================
# 5. IDENTIFY IMPORTANT COLUMNS
# ============================================================

product_id_col = first_existing(
    [
        "product_id"
    ]
)

quantity_col = first_existing(
    [
        "total_quantity_sold",
        "quantity",
        "total_quantity"
    ]
)

sales_value_col = first_existing(
    [
        "total_sales_value",
        "sales_value",
        "revenue",
        "total_revenue"
    ]
)

stock_col = first_existing(
    [
        "current_stock",
        "stock_quantity"
    ]
)

inventory_cost_col = first_existing(
    [
        "inventory_cost_value",
        "inventory_value_at_cost"
    ]
)

inventory_retail_col = first_existing(
    [
        "inventory_retail_value",
        "inventory_value_at_retail"
    ]
)

margin_col = first_existing(
    [
        "unit_margin",
        "total_margin"
    ]
)


# ============================================================
# 6. BASIC KPI CALCULATIONS
# ============================================================

total_products = (
    df[product_id_col].nunique()
    if product_id_col
    else len(df)
)

total_quantity_sold = numeric_sum(
    quantity_col
)

total_sales_value = numeric_sum(
    sales_value_col
)

total_current_stock = numeric_sum(
    stock_col
)

total_inventory_cost = numeric_sum(
    inventory_cost_col
)

total_inventory_retail = numeric_sum(
    inventory_retail_col
)

total_margin = numeric_sum(
    margin_col
)


# ============================================================
# 7. AVERAGE SELLING PRICE
# ============================================================

if (
    sales_value_col
    and quantity_col
    and total_quantity_sold != 0
):

    average_selling_price = (
        total_sales_value /
        total_quantity_sold
    )

else:

    average_selling_price = 0


# ============================================================
# 8. INVENTORY VALUE
# ============================================================

if total_inventory_cost != 0:

    inventory_value_growth = (
        (
            total_inventory_retail
            - total_inventory_cost
        )
        / total_inventory_cost
    ) * 100

else:

    inventory_value_growth = 0


# ============================================================
# 9. STOCK / SALES RATIO
# ============================================================

if total_quantity_sold != 0:

    stock_to_sales_ratio = (
        total_current_stock /
        total_quantity_sold
    )

else:

    stock_to_sales_ratio = 0


# ============================================================
# 10. REORDER RISK
# ============================================================

reorder_risk_count = 0

if "reorder_risk_flag" in df.columns:

    reorder_values = (
        df["reorder_risk_flag"]
        .astype(str)
        .str.lower()
    )

    reorder_risk_count = int(
        reorder_values.isin(
            [
                "1",
                "true",
                "yes",
                "risk",
                "reorder"
            ]
        ).sum()
    )


# ============================================================
# 11. OVERSTOCK COUNT
# ============================================================

overstock_count = 0

if "overstock_flag" in df.columns:

    overstock_values = (
        df["overstock_flag"]
        .astype(str)
        .str.lower()
    )

    overstock_count = int(
        overstock_values.isin(
            [
                "1",
                "true",
                "yes",
                "overstock"
            ]
        ).sum()
    )


# ============================================================
# 12. DEMAND LEVEL DISTRIBUTION
# ============================================================

demand_distribution = pd.DataFrame()

if "demand_level" in df.columns:

    demand_distribution = (
        df["demand_level"]
        .value_counts(dropna=False)
        .reset_index()
    )

    demand_distribution.columns = [
        "demand_level",
        "product_count"
    ]


# ============================================================
# 13. TOP DEMAND PRODUCTS
# ============================================================

top_products = pd.DataFrame()

if (
    product_id_col
    and quantity_col
):

    top_products = (
        df[
            [
                product_id_col,
                quantity_col
            ]
        ]
        .copy()
        .sort_values(
            quantity_col,
            ascending=False
        )
        .head(10)
    )

    top_products.columns = [
        "product_id",
        "quantity_sold"
    ]


# ============================================================
# 14. KPI SUMMARY
# ============================================================

kpi_summary = pd.DataFrame(
    {
        "kpi": [
            "total_products",
            "total_quantity_sold",
            "total_sales_value",
            "total_current_stock",
            "total_inventory_cost",
            "total_inventory_retail_value",
            "total_margin",
            "average_selling_price",
            "stock_to_sales_ratio",
            "reorder_risk_products",
            "overstock_products",
            "inventory_value_growth_percentage"
        ],
        "value": [
            total_products,
            total_quantity_sold,
            total_sales_value,
            total_current_stock,
            total_inventory_cost,
            total_inventory_retail,
            total_margin,
            average_selling_price,
            stock_to_sales_ratio,
            reorder_risk_count,
            overstock_count,
            inventory_value_growth
        ]
    }
)


# ============================================================
# 15. SAVE KPI SUMMARY
# ============================================================

KPI_SUMMARY_FILE = (
    KPI_DIR /
    "week03_kpi_summary.csv"
)

kpi_summary.to_csv(
    KPI_SUMMARY_FILE,
    index=False
)


# ============================================================
# 16. SAVE TOP PRODUCTS
# ============================================================

TOP_PRODUCTS_FILE = (
    KPI_DIR /
    "week03_top_demand_products.csv"
)

top_products.to_csv(
    TOP_PRODUCTS_FILE,
    index=False
)


# ============================================================
# 17. SAVE DEMAND DISTRIBUTION
# ============================================================

DEMAND_FILE = (
    KPI_DIR /
    "week03_demand_distribution.csv"
)

demand_distribution.to_csv(
    DEMAND_FILE,
    index=False
)


# ============================================================
# 18. FINAL OUTPUT
# ============================================================

print()
print("=" * 70)
print("WEEK 03 - FIRST KPI ANALYSIS COMPLETE")
print("=" * 70)

print(f"Total products: {total_products}")
print(f"Total quantity sold: {total_quantity_sold}")
print(f"Total sales value: {total_sales_value}")
print(f"Total current stock: {total_current_stock}")
print(f"Reorder-risk products: {reorder_risk_count}")
print(f"Overstock products: {overstock_count}")

print()
print(
    f"KPI summary saved: {KPI_SUMMARY_FILE}"
)

print(
    f"Top demand products saved: {TOP_PRODUCTS_FILE}"
)

print(
    f"Demand distribution saved: {DEMAND_FILE}"
)

print()
print(
    "All first KPI outputs generated successfully."
)