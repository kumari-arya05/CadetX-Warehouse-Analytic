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
# DATE CONVERSION
# ---------------------------------------------------------
purchase_orders["order_date"] = pd.to_datetime(
    purchase_orders["order_date"],
    errors="coerce"
)

purchase_orders["expected_delivery_date"] = pd.to_datetime(
    purchase_orders["expected_delivery_date"],
    errors="coerce"
)

purchase_orders["received_date"] = pd.to_datetime(
    purchase_orders["received_date"],
    errors="coerce"
)

# ---------------------------------------------------------
# DELIVERY CALCULATIONS
# ---------------------------------------------------------
purchase_orders["actual_delivery_days"] = (
    purchase_orders["received_date"]
    - purchase_orders["order_date"]
).dt.days

purchase_orders["expected_delivery_days"] = (
    purchase_orders["expected_delivery_date"]
    - purchase_orders["order_date"]
).dt.days

purchase_orders["delivery_delay_days"] = (
    purchase_orders["actual_delivery_days"]
    - purchase_orders["expected_delivery_days"]
)

# ---------------------------------------------------------
# ON-TIME DELIVERY FLAG
# ---------------------------------------------------------
purchase_orders["on_time_delivery"] = (
    purchase_orders["delivery_delay_days"] <= 0
)

# ---------------------------------------------------------
# SUPPLIER RELIABILITY ANALYSIS
# ---------------------------------------------------------
supplier_reliability = (
    purchase_orders
    .groupby("supplier_id")
    .agg(
        total_orders=("po_id", "count"),
        on_time_orders=("on_time_delivery", "sum"),
        average_delivery_days=(
            "actual_delivery_days",
            "mean"
        ),
        average_delay_days=(
            "delivery_delay_days",
            "mean"
        )
    )
    .reset_index()
)

# ---------------------------------------------------------
# ON-TIME DELIVERY RATE
# ---------------------------------------------------------
supplier_reliability["on_time_delivery_rate"] = (
    supplier_reliability["on_time_orders"]
    / supplier_reliability["total_orders"]
    * 100
)

# ---------------------------------------------------------
# RELIABILITY RATING
# ---------------------------------------------------------
def reliability_rating(rate):
    if rate >= 90:
        return "Excellent"
    elif rate >= 75:
        return "Good"
    elif rate >= 60:
        return "Average"
    else:
        return "Poor"


supplier_reliability["reliability_rating"] = (
    supplier_reliability["on_time_delivery_rate"]
    .apply(reliability_rating)
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

supplier_reliability = supplier_details.merge(
    supplier_reliability,
    on="supplier_id",
    how="left"
)

# ---------------------------------------------------------
# ROUND VALUES
# ---------------------------------------------------------
supplier_reliability["average_delivery_days"] = (
    supplier_reliability["average_delivery_days"]
    .round(2)
)

supplier_reliability["average_delay_days"] = (
    supplier_reliability["average_delay_days"]
    .round(2)
)

supplier_reliability["on_time_delivery_rate"] = (
    supplier_reliability["on_time_delivery_rate"]
    .round(2)
)

# ---------------------------------------------------------
# SORT BY RELIABILITY
# ---------------------------------------------------------
supplier_reliability = supplier_reliability.sort_values(
    by="on_time_delivery_rate",
    ascending=False
)

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("SUPPLIER RELIABILITY ANALYSIS")
print("=" * 70)

print("\nSupplier Reliability:")
print(
    supplier_reliability.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUT
# ---------------------------------------------------------
output_file = (
    OUTPUT_DIR / "supplier_reliability_analysis.csv"
)

supplier_reliability.to_csv(
    output_file,
    index=False
)

# ---------------------------------------------------------
# SUCCESS MESSAGE
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("Supplier Reliability Analysis completed successfully.")
print(f"Output saved to: {output_file}")
print("=" * 70)