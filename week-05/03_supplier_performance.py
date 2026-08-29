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
# Supplier Performance Analysis
# --------------------------------------------------

performance = (
    purchase_orders
    .groupby("supplier_id", as_index=False)
    .agg(
        purchase_order_count=("po_id", "nunique"),
        total_purchase_value=("grand_total", "sum"),
        average_purchase_value=("grand_total", "mean"),
        total_purchase_cost=("total_cost", "sum")
    )
)


# --------------------------------------------------
# Add Supplier Information
# --------------------------------------------------

performance = performance.merge(
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
# Performance Components
# --------------------------------------------------

performance["purchase_value_score"] = (
    performance["total_purchase_value"]
    / performance["total_purchase_value"].max()
    * 100
)

performance["reliability_score_normalised"] = (
    performance["reliability_score"]
    / performance["reliability_score"].max()
    * 100
)

performance["lead_time_score"] = (
    1
    - (
        performance["lead_time_days"]
        / performance["lead_time_days"].max()
    )
) * 100


# --------------------------------------------------
# Overall Supplier Performance Score
# --------------------------------------------------

performance["performance_score"] = (
    performance["purchase_value_score"] * 0.40
    + performance["reliability_score_normalised"] * 0.40
    + performance["lead_time_score"] * 0.20
)


# --------------------------------------------------
# Performance Category
# --------------------------------------------------

performance["performance_category"] = pd.cut(
    performance["performance_score"],
    bins=[-float("inf"), 40, 60, 80, float("inf")],
    labels=[
        "Low Performance",
        "Moderate Performance",
        "High Performance",
        "Very High Performance"
    ]
)


# --------------------------------------------------
# Performance Ranking
# --------------------------------------------------

performance = performance.sort_values(
    "performance_score",
    ascending=False
).reset_index(drop=True)

performance["performance_rank"] = performance.index + 1


# --------------------------------------------------
# Save Output
# --------------------------------------------------

output_file = OUTPUT_DIR / "supplier_performance.csv"

performance.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("Supplier Performance Analysis completed successfully.")
print(f"Suppliers analysed: {len(performance)}")
print(f"Output saved to: {output_file}")

print("\nTop 10 Suppliers by Performance:")
print(
    performance[
        [
            "supplier_id",
            "supplier_name",
            "purchase_order_count",
            "total_purchase_value",
            "reliability_score",
            "lead_time_days",
            "performance_score",
            "performance_category",
            "performance_rank"
        ]
    ].head(10).to_string(index=False)
)