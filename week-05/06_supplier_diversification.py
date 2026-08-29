import pandas as pd
from pathlib import Path


# --------------------------------------------------
# File Paths
# --------------------------------------------------

SUPPLIER_FILE = Path("data/cleaned/suppliers.csv")
PURCHASE_ORDER_FILE = Path("data/cleaned/purchase_orders_header.csv")

OUTPUT_DIR = Path("data/features")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load Data
# --------------------------------------------------

suppliers = pd.read_csv(SUPPLIER_FILE)
purchase_orders = pd.read_csv(PURCHASE_ORDER_FILE)


# --------------------------------------------------
# Supplier Diversification Analysis
# --------------------------------------------------

diversification = (
    suppliers[
        [
            "supplier_id",
            "supplier_name",
            "supplier_type",
            "product_category",
            "region"
        ]
    ]
    .groupby(
        ["product_category", "region"],
        as_index=False
    )
    .agg(
        supplier_count=("supplier_id", "nunique")
    )
)


# --------------------------------------------------
# Category-Level Supplier Coverage
# --------------------------------------------------

category_supplier_count = (
    suppliers
    .groupby("product_category", as_index=False)
    .agg(
        supplier_count=("supplier_id", "nunique"),
        region_count=("region", "nunique")
    )
)


# --------------------------------------------------
# Purchase Value by Supplier and Category
# --------------------------------------------------

supplier_category_value = (
    purchase_orders
    .merge(
        suppliers[
            [
                "supplier_id",
                "supplier_name",
                "product_category"
            ]
        ],
        on="supplier_id",
        how="left"
    )
    .groupby(
        ["product_category", "supplier_id", "supplier_name"],
        as_index=False
    )
    .agg(
        purchase_order_count=("po_id", "nunique"),
        total_purchase_value=("grand_total", "sum")
    )
)


# --------------------------------------------------
# Supplier Share within Product Category
# --------------------------------------------------

category_totals = (
    supplier_category_value
    .groupby("product_category")["total_purchase_value"]
    .transform("sum")
)

supplier_category_value["category_purchase_share"] = (
    supplier_category_value["total_purchase_value"]
    / category_totals
    * 100
)


# --------------------------------------------------
# Supplier Rank within Category
# --------------------------------------------------

supplier_category_value = supplier_category_value.sort_values(
    ["product_category", "total_purchase_value"],
    ascending=[True, False]
).reset_index(drop=True)

supplier_category_value["supplier_category_rank"] = (
    supplier_category_value
    .groupby("product_category")
    .cumcount()
    + 1
)


# --------------------------------------------------
# Diversification Risk
# --------------------------------------------------

supplier_category_value["diversification_risk"] = pd.cut(
    supplier_category_value["category_purchase_share"],
    bins=[-float("inf"), 40, 60, 80, float("inf")],
    labels=[
        "Low Concentration",
        "Moderate Concentration",
        "High Concentration",
        "Critical Concentration"
    ]
)


# --------------------------------------------------
# Category Supplier Count
# --------------------------------------------------

supplier_category_value = supplier_category_value.merge(
    category_supplier_count,
    on="product_category",
    how="left"
)


# --------------------------------------------------
# Diversification Status
# --------------------------------------------------

supplier_category_value["diversification_status"] = (
    supplier_category_value["supplier_count"]
    .apply(
        lambda x:
        "Well Diversified" if x >= 3
        else "Moderately Diversified" if x == 2
        else "Single Supplier Dependency"
    )
)


# --------------------------------------------------
# Save Output
# --------------------------------------------------

output_file = OUTPUT_DIR / "supplier_diversification.csv"

supplier_category_value.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("Supplier Diversification Analysis completed successfully.")
print(f"Product categories analysed: {supplier_category_value['product_category'].nunique()}")
print(f"Suppliers analysed: {supplier_category_value['supplier_id'].nunique()}")
print(f"Output saved to: {output_file}")

print("\nSupplier Diversification Summary:")
print(
    supplier_category_value[
        [
            "product_category",
            "supplier_count",
            "supplier_id",
            "supplier_name",
            "total_purchase_value",
            "category_purchase_share",
            "diversification_risk",
            "diversification_status"
        ]
    ]
    .head(15)
    .to_string(index=False)
)