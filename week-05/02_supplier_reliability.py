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
# Supplier Reliability Analysis
# --------------------------------------------------

reliability = (
    purchase_orders
    .groupby("supplier_id", as_index=False)
    .agg(
        purchase_order_count=("po_id", "nunique"),
        total_purchase_value=("grand_total", "sum"),
        expected_delivery_date_count=("expected_delivery_date", "count"),
        received_date_count=("received_date", "count")
    )
)


# --------------------------------------------------
# Delivery Completion Rate
# --------------------------------------------------

reliability["delivery_completion_rate"] = (
    reliability["received_date_count"]
    / reliability["expected_delivery_date_count"]
    * 100
)

reliability["delivery_completion_rate"] = (
    reliability["delivery_completion_rate"].fillna(0)
)


# --------------------------------------------------
# Add Supplier Information
# --------------------------------------------------

reliability = reliability.merge(
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
# Reliability Category
# --------------------------------------------------

reliability["reliability_category"] = pd.cut(
    reliability["reliability_score"],
    bins=[-float("inf"), 0.60, 0.80, 0.90, float("inf")],
    labels=[
        "Low Reliability",
        "Moderate Reliability",
        "High Reliability",
        "Very High Reliability"
    ]
)


# --------------------------------------------------
# Reliability Ranking
# --------------------------------------------------

reliability = reliability.sort_values(
    ["reliability_score", "delivery_completion_rate"],
    ascending=False
).reset_index(drop=True)

reliability["reliability_rank"] = reliability.index + 1


# --------------------------------------------------
# Save Output
# --------------------------------------------------

output_file = OUTPUT_DIR / "supplier_reliability.csv"

reliability.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("Supplier Reliability Analysis completed successfully.")
print(f"Suppliers analysed: {len(reliability)}")
print(f"Output saved to: {output_file}")

print("\nTop 10 Suppliers by Reliability:")
print(
    reliability[
        [
            "supplier_id",
            "supplier_name",
            "purchase_order_count",
            "reliability_score",
            "delivery_completion_rate",
            "reliability_category",
            "reliability_rank"
        ]
    ].head(10).to_string(index=False)
)