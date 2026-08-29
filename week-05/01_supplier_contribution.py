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
# Supplier Contribution Analysis
# --------------------------------------------------

supplier_contribution = (
    purchase_orders
    .groupby("supplier_id", as_index=False)
    .agg(
        purchase_order_count=("po_id", "nunique"),
        total_purchase_cost=("total_cost", "sum"),
        total_gst_amount=("total_gst_amount", "sum"),
        total_purchase_value=("grand_total", "sum")
    )
)


# --------------------------------------------------
# Add Supplier Information
# --------------------------------------------------

supplier_contribution = supplier_contribution.merge(
    suppliers[
        [
            "supplier_id",
            "supplier_name",
            "supplier_type",
            "product_category",
            "city",
            "province",
            "region",
            "lead_time_days",
            "reliability_score"
        ]
    ],
    on="supplier_id",
    how="left"
)


# --------------------------------------------------
# Contribution Percentage
# --------------------------------------------------

total_value = supplier_contribution["total_purchase_value"].sum()

supplier_contribution["contribution_percentage"] = (
    supplier_contribution["total_purchase_value"]
    / total_value
    * 100
)


# --------------------------------------------------
# Supplier Ranking
# --------------------------------------------------

supplier_contribution = supplier_contribution.sort_values(
    "total_purchase_value",
    ascending=False
).reset_index(drop=True)

supplier_contribution["contribution_rank"] = (
    supplier_contribution.index + 1
)


# --------------------------------------------------
# Contribution Category
# --------------------------------------------------

supplier_contribution["contribution_category"] = pd.cut(
    supplier_contribution["contribution_percentage"],
    bins=[-float("inf"), 1, 5, 10, float("inf")],
    labels=[
        "Low Contribution",
        "Moderate Contribution",
        "High Contribution",
        "Very High Contribution"
    ]
)


# --------------------------------------------------
# Save Output
# --------------------------------------------------

output_file = OUTPUT_DIR / "supplier_contribution.csv"

supplier_contribution.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("Supplier Contribution Analysis completed successfully.")
print(f"Suppliers analysed: {len(supplier_contribution)}")
print(f"Output saved to: {output_file}")

print("\nTop 10 Suppliers by Purchase Value:")
print(
    supplier_contribution[
        [
            "supplier_id",
            "supplier_name",
            "purchase_order_count",
            "total_purchase_value",
            "contribution_percentage",
            "contribution_rank"
        ]
    ].head(10).to_string(index=False)
)