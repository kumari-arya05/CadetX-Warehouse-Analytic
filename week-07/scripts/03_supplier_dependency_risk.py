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
# CALCULATE SUPPLIER PURCHASE VALUE
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
# DEPENDENCY PERCENTAGE
# ---------------------------------------------------------
supplier_purchase["order_dependency_percentage"] = (
    supplier_purchase["total_orders"]
    / supplier_purchase["total_orders"].sum()
    * 100
)

supplier_purchase["value_dependency_percentage"] = (
    supplier_purchase["total_purchase_value"]
    / total_purchase_value
    * 100
)

# ---------------------------------------------------------
# RISK SCORE
# ---------------------------------------------------------
def calculate_risk(value_dependency):
    if value_dependency >= 30:
        return 3
    elif value_dependency >= 20:
        return 2
    elif value_dependency >= 10:
        return 1
    else:
        return 0


supplier_purchase["dependency_risk_score"] = (
    supplier_purchase["value_dependency_percentage"]
    .apply(calculate_risk)
)

# ---------------------------------------------------------
# RISK CLASSIFICATION
# ---------------------------------------------------------
def risk_classification(score):
    if score == 3:
        return "High Risk"
    elif score == 2:
        return "Medium Risk"
    elif score == 1:
        return "Low Risk"
    else:
        return "Minimal Risk"


supplier_purchase["dependency_risk"] = (
    supplier_purchase["dependency_risk_score"]
    .apply(risk_classification)
)

# ---------------------------------------------------------
# CRITICAL SUPPLIER FLAG
# ---------------------------------------------------------
supplier_purchase["critical_supplier"] = (
    supplier_purchase["value_dependency_percentage"] >= 20
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
        "reliability_score"
    ]
].drop_duplicates(
    subset=["supplier_id"]
)

supplier_dependency = supplier_details.merge(
    supplier_purchase,
    on="supplier_id",
    how="left"
)

# ---------------------------------------------------------
# ROUND VALUES
# ---------------------------------------------------------
supplier_dependency["total_purchase_value"] = (
    supplier_dependency["total_purchase_value"]
    .round(2)
)

supplier_dependency["order_dependency_percentage"] = (
    supplier_dependency["order_dependency_percentage"]
    .round(2)
)

supplier_dependency["value_dependency_percentage"] = (
    supplier_dependency["value_dependency_percentage"]
    .round(2)
)

# ---------------------------------------------------------
# SORT BY DEPENDENCY
# ---------------------------------------------------------
supplier_dependency = supplier_dependency.sort_values(
    by="value_dependency_percentage",
    ascending=False
)

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("SUPPLIER DEPENDENCY RISK ANALYSIS")
print("=" * 70)

print("\nSupplier Dependency Risk:")
print(
    supplier_dependency.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUT
# ---------------------------------------------------------
output_file = (
    OUTPUT_DIR / "supplier_dependency_risk.csv"
)

supplier_dependency.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 70)
print("Supplier Dependency Risk Analysis completed successfully.")
print(f"Output saved to: {output_file}")
print("=" * 70)