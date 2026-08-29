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
# Supplier Purchase Analysis
# --------------------------------------------------

critical = (
    purchase_orders
    .groupby("supplier_id", as_index=False)
    .agg(
        purchase_order_count=("po_id", "nunique"),
        total_purchase_value=("grand_total", "sum"),
        average_purchase_value=("grand_total", "mean")
    )
)


# --------------------------------------------------
# Add Supplier Information
# --------------------------------------------------

critical = critical.merge(
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
# Purchase Contribution
# --------------------------------------------------

total_purchase_value = critical["total_purchase_value"].sum()

critical["purchase_contribution_percentage"] = (
    critical["total_purchase_value"]
    / total_purchase_value
    * 100
)


# --------------------------------------------------
# Critical Supplier Indicators
# --------------------------------------------------

critical["high_contribution"] = (
    critical["purchase_contribution_percentage"] >= 10
)

critical["high_lead_time"] = (
    critical["lead_time_days"]
    >= critical["lead_time_days"].median()
)

critical["low_reliability"] = (
    critical["reliability_score"]
    < critical["reliability_score"].median()
)


# --------------------------------------------------
# Critical Indicator Count
# --------------------------------------------------

critical["critical_indicator_count"] = (
    critical["high_contribution"].astype(int)
    + critical["high_lead_time"].astype(int)
    + critical["low_reliability"].astype(int)
)


# --------------------------------------------------
# Critical Supplier Status
# --------------------------------------------------

critical["critical_supplier_status"] = critical[
    "critical_indicator_count"
].apply(
    lambda x: "Critical Supplier" if x >= 2 else "Non-Critical Supplier"
)


# --------------------------------------------------
# Critical Supplier Risk Level
# --------------------------------------------------

critical["risk_level"] = pd.cut(
    critical["critical_indicator_count"],
    bins=[-1, 0, 1, 2, 3],
    labels=[
        "Low",
        "Moderate",
        "High",
        "Critical"
    ]
)


# --------------------------------------------------
# Priority Ranking
# --------------------------------------------------

critical = critical.sort_values(
    [
        "critical_indicator_count",
        "purchase_contribution_percentage"
    ],
    ascending=[False, False]
).reset_index(drop=True)

critical["critical_supplier_rank"] = critical.index + 1


# --------------------------------------------------
# Save Output
# --------------------------------------------------

output_file = OUTPUT_DIR / "critical_supplier_identification.csv"

critical.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("Critical Supplier Identification completed successfully.")
print(f"Suppliers analysed: {len(critical)}")
print(
    f"Critical suppliers identified: "
    f"{(critical['critical_supplier_status'] == 'Critical Supplier').sum()}"
)
print(f"Output saved to: {output_file}")

print("\nCritical Suppliers:")
print(
    critical[
        [
            "supplier_id",
            "supplier_name",
            "total_purchase_value",
            "purchase_contribution_percentage",
            "lead_time_days",
            "reliability_score",
            "critical_indicator_count",
            "critical_supplier_status",
            "risk_level",
            "critical_supplier_rank"
        ]
    ]
    .query("critical_supplier_status == 'Critical Supplier'")
    .to_string(index=False)
)