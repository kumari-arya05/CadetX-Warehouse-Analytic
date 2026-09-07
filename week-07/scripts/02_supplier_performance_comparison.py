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
suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
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
# DELIVERY PERFORMANCE
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

purchase_orders["on_time"] = (
    purchase_orders["delivery_delay_days"] <= 0
)

# ---------------------------------------------------------
# SUPPLIER PERFORMANCE
# ---------------------------------------------------------
supplier_performance = (
    purchase_orders
    .groupby("supplier_id")
    .agg(
        total_orders=("po_id", "count"),
        on_time_orders=("on_time", "sum"),
        average_delivery_days=(
            "actual_delivery_days",
            "mean"
        ),
        average_delay_days=(
            "delivery_delay_days",
            "mean"
        ),
        total_purchase_cost=(
            "total_cost",
            "sum"
        ),
        average_order_value=(
            "total_cost",
            "mean"
        )
    )
    .reset_index()
)

# ---------------------------------------------------------
# ON-TIME DELIVERY RATE
# ---------------------------------------------------------
supplier_performance["on_time_delivery_rate"] = (
    supplier_performance["on_time_orders"]
    / supplier_performance["total_orders"]
    * 100
)

# ---------------------------------------------------------
# PERFORMANCE RATING
# ---------------------------------------------------------
def performance_rating(rate):
    if rate >= 90:
        return "Excellent"
    elif rate >= 75:
        return "Good"
    elif rate >= 60:
        return "Average"
    else:
        return "Poor"


supplier_performance["performance_rating"] = (
    supplier_performance["on_time_delivery_rate"]
    .apply(performance_rating)
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

supplier_performance = supplier_details.merge(
    supplier_performance,
    on="supplier_id",
    how="left"
)

# ---------------------------------------------------------
# ROUND NUMERIC VALUES
# ---------------------------------------------------------
supplier_performance["average_delivery_days"] = (
    supplier_performance["average_delivery_days"]
    .round(2)
)

supplier_performance["average_delay_days"] = (
    supplier_performance["average_delay_days"]
    .round(2)
)

supplier_performance["total_purchase_cost"] = (
    supplier_performance["total_purchase_cost"]
    .round(2)
)

supplier_performance["average_order_value"] = (
    supplier_performance["average_order_value"]
    .round(2)
)

supplier_performance["on_time_delivery_rate"] = (
    supplier_performance["on_time_delivery_rate"]
    .round(2)
)

# ---------------------------------------------------------
# SORT BY PERFORMANCE
# ---------------------------------------------------------
supplier_performance = supplier_performance.sort_values(
    by="on_time_delivery_rate",
    ascending=False
)

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("SUPPLIER PERFORMANCE COMPARISON")
print("=" * 70)

print("\nSupplier Performance:")
print(
    supplier_performance.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUT
# ---------------------------------------------------------
output_file = (
    OUTPUT_DIR / "supplier_performance_comparison.csv"
)

supplier_performance.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 70)
print("Supplier Performance Comparison completed successfully.")
print(f"Output saved to: {output_file}")
print("=" * 70)