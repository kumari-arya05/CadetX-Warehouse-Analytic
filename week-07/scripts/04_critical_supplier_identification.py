import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
suppliers = pd.read_csv(
    DATA_DIR / "suppliers.csv"
)

purchase_orders = pd.read_csv(
    DATA_DIR / "purchase_orders_header.csv"
)

# ---------------------------------------------------------
# SUPPLIER PURCHASE VALUE
# ---------------------------------------------------------
supplier_purchase = (
    purchase_orders
    .groupby("supplier_id")
    .agg(
        total_orders=("po_id", "count"),
        total_purchase_value=("total_cost", "sum")
    )
    .reset_index()
)

# ---------------------------------------------------------
# TOTAL PURCHASE VALUE
# ---------------------------------------------------------
total_purchase_value = supplier_purchase[
    "total_purchase_value"
].sum()

# ---------------------------------------------------------
# PURCHASE VALUE SHARE
# ---------------------------------------------------------
supplier_purchase["purchase_value_share"] = (
    supplier_purchase["total_purchase_value"]
    / total_purchase_value
    * 100
)

# ---------------------------------------------------------
# MERGE SUPPLIER DETAILS
# ---------------------------------------------------------
supplier_details = suppliers[
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
].drop_duplicates(
    subset=["supplier_id"]
)

critical_suppliers = supplier_details.merge(
    supplier_purchase,
    on="supplier_id",
    how="left"
)

# ---------------------------------------------------------
# CRITICAL SUPPLIER IDENTIFICATION
# ---------------------------------------------------------
# A supplier is considered critical if:
# 1. Purchase value share is 20% or more
# OR
# 2. Reliability score is below 60
critical_suppliers["critical_supplier"] = (
    (critical_suppliers["purchase_value_share"] >= 20)
    |
    (critical_suppliers["reliability_score"] < 60)
)

# ---------------------------------------------------------
# CRITICALITY REASON
# ---------------------------------------------------------
def identify_reason(row):
    reasons = []

    if row["purchase_value_share"] >= 20:
        reasons.append("High Purchase Dependency")

    if row["reliability_score"] < 60:
        reasons.append("Low Reliability")

    if not reasons:
        return "Normal"

    return " & ".join(reasons)


critical_suppliers["criticality_reason"] = (
    critical_suppliers.apply(
        identify_reason,
        axis=1
    )
)

# ---------------------------------------------------------
# RISK LEVEL
# ---------------------------------------------------------
def risk_level(row):
    if (
        row["purchase_value_share"] >= 20
        and row["reliability_score"] < 60
    ):
        return "High Risk"

    elif (
        row["purchase_value_share"] >= 20
        or row["reliability_score"] < 60
    ):
        return "Medium Risk"

    else:
        return "Low Risk"


critical_suppliers["risk_level"] = (
    critical_suppliers.apply(
        risk_level,
        axis=1
    )
)

# ---------------------------------------------------------
# ROUND VALUES
# ---------------------------------------------------------
critical_suppliers["total_purchase_value"] = (
    critical_suppliers["total_purchase_value"]
    .round(2)
)

critical_suppliers["purchase_value_share"] = (
    critical_suppliers["purchase_value_share"]
    .round(2)
)

# ---------------------------------------------------------
# SORT RESULTS
# ---------------------------------------------------------
critical_suppliers = critical_suppliers.sort_values(
    by=[
        "critical_supplier",
        "purchase_value_share"
    ],
    ascending=[False, False]
)

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("CRITICAL SUPPLIER IDENTIFICATION")
print("=" * 70)

print("\nCritical Suppliers:")

print(
    critical_suppliers[
        [
            "supplier_id",
            "supplier_name",
            "total_orders",
            "total_purchase_value",
            "purchase_value_share",
            "reliability_score",
            "critical_supplier",
            "criticality_reason",
            "risk_level"
        ]
    ].to_string(index=False)
)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------
total_suppliers = len(critical_suppliers)

critical_count = (
    critical_suppliers["critical_supplier"].sum()
)

summary = pd.DataFrame({
    "metric": [
        "Total Suppliers",
        "Critical Suppliers",
        "Critical Supplier Percentage"
    ],
    "value": [
        total_suppliers,
        int(critical_count),
        round(
            critical_count / total_suppliers * 100,
            2
        )
    ]
})

print("\nCritical Supplier Summary:")
print(
    summary.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------------
output_file = (
    OUTPUT_DIR / "critical_supplier_identification.csv"
)

summary_file = (
    OUTPUT_DIR / "critical_supplier_summary.csv"
)

critical_suppliers.to_csv(
    output_file,
    index=False
)

summary.to_csv(
    summary_file,
    index=False
)

print("\n" + "=" * 70)
print("Critical Supplier Identification completed successfully.")
print(f"Supplier output saved to: {output_file}")
print(f"Summary output saved to: {summary_file}")
print("=" * 70)