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
# Supplier Purchase Contribution
# --------------------------------------------------

dependency = (
    purchase_orders
    .groupby("supplier_id", as_index=False)
    .agg(
        purchase_order_count=("po_id", "nunique"),
        total_purchase_value=("grand_total", "sum")
    )
)


# --------------------------------------------------
# Calculate Dependency Percentage
# --------------------------------------------------

total_purchase_value = dependency["total_purchase_value"].sum()

dependency["dependency_percentage"] = (
    dependency["total_purchase_value"]
    / total_purchase_value
    * 100
)


# --------------------------------------------------
# Add Supplier Information
# --------------------------------------------------

dependency = dependency.merge(
    suppliers[
        [
            "supplier_id",
            "supplier_name",
            "supplier_type",
            "product_category",
            "lead_time_days",
            "reliability_score"
        ]
    ],
    on="supplier_id",
    how="left"
)


# --------------------------------------------------
# Dependency Risk Category
# --------------------------------------------------

dependency["dependency_risk"] = pd.cut(
    dependency["dependency_percentage"],
    bins=[-float("inf"), 5, 10, 20, float("inf")],
    labels=[
        "Low Dependency Risk",
        "Moderate Dependency Risk",
        "High Dependency Risk",
        "Critical Dependency Risk"
    ]
)


# --------------------------------------------------
# Risk Score
# --------------------------------------------------

dependency["dependency_risk_score"] = (
    dependency["dependency_percentage"]
    / dependency["dependency_percentage"].max()
    * 100
)


# --------------------------------------------------
# Dependency Ranking
# --------------------------------------------------

dependency = dependency.sort_values(
    "dependency_percentage",
    ascending=False
).reset_index(drop=True)

dependency["dependency_rank"] = dependency.index + 1


# --------------------------------------------------
# Save Output
# --------------------------------------------------

output_file = OUTPUT_DIR / "supplier_dependency_risk.csv"

dependency.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("Supplier Dependency Risk Analysis completed successfully.")
print(f"Suppliers analysed: {len(dependency)}")
print(f"Output saved to: {output_file}")

print("\nTop 10 Suppliers by Dependency:")
print(
    dependency[
        [
            "supplier_id",
            "supplier_name",
            "purchase_order_count",
            "total_purchase_value",
            "dependency_percentage",
            "dependency_risk",
            "dependency_risk_score",
            "dependency_rank"
        ]
    ].head(10).to_string(index=False)
)