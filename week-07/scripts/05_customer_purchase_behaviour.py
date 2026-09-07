
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
# LOAD SALES ORDER DATA
# ---------------------------------------------------------
sales_orders = pd.read_csv(
    DATA_DIR / "sales_orders_header.csv"
)

# ---------------------------------------------------------
# DATE CONVERSION
# ---------------------------------------------------------
sales_orders["order_date"] = pd.to_datetime(
    sales_orders["order_date"],
    errors="coerce"
)

# Remove invalid customer IDs or dates
sales_orders = sales_orders.dropna(
    subset=["customer_id", "order_date"]
)

# ---------------------------------------------------------
# CUSTOMER PURCHASE BEHAVIOUR
# ---------------------------------------------------------
customer_behaviour = (
    sales_orders
    .groupby("customer_id")
    .agg(
        total_orders=("so_id", "count"),
        total_order_value=("total_order_value", "sum"),
        average_order_value=("total_order_value", "mean"),
        first_order_date=("order_date", "min"),
        last_order_date=("order_date", "max")
    )
    .reset_index()
)

# ---------------------------------------------------------
# CUSTOMER ACTIVITY DAYS
# ---------------------------------------------------------
customer_behaviour["activity_days"] = (
    customer_behaviour["last_order_date"]
    - customer_behaviour["first_order_date"]
).dt.days

# ---------------------------------------------------------
# PURCHASE BEHAVIOUR CLASSIFICATION
# ---------------------------------------------------------
def classify_behaviour(order_count):
    if order_count >= 10:
        return "Highly Frequent"
    elif order_count >= 5:
        return "Frequent"
    elif order_count >= 2:
        return "Repeat"
    else:
        return "One-Time"


customer_behaviour["purchase_behaviour"] = (
    customer_behaviour["total_orders"]
    .apply(classify_behaviour)
)

# ---------------------------------------------------------
# ROUND VALUES
# ---------------------------------------------------------
customer_behaviour["total_order_value"] = (
    customer_behaviour["total_order_value"]
    .round(2)
)

customer_behaviour["average_order_value"] = (
    customer_behaviour["average_order_value"]
    .round(2)
)

# ---------------------------------------------------------
# SORT CUSTOMERS
# ---------------------------------------------------------
customer_behaviour = customer_behaviour.sort_values(
    by="total_order_value",
    ascending=False
)

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("CUSTOMER PURCHASE BEHAVIOUR ANALYSIS")
print("=" * 70)

print("\nCustomer Purchase Behaviour:")

print(
    customer_behaviour.head(20).to_string(
        index=False
    )
)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------
behaviour_summary = (
    customer_behaviour
    .groupby("purchase_behaviour")
    .agg(
        customers=("customer_id", "nunique"),
        total_orders=("total_orders", "sum"),
        total_order_value=("total_order_value", "sum"),
        average_order_value=("average_order_value", "mean")
    )
    .reset_index()
)

behaviour_summary["total_order_value"] = (
    behaviour_summary["total_order_value"]
    .round(2)
)

behaviour_summary["average_order_value"] = (
    behaviour_summary["average_order_value"]
    .round(2)
)

print("\nPurchase Behaviour Summary:")

print(
    behaviour_summary.to_string(
        index=False
    )
)

# ---------------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------------
customer_output = (
    OUTPUT_DIR / "customer_purchase_behaviour.csv"
)

summary_output = (
    OUTPUT_DIR / "customer_purchase_behaviour_summary.csv"
)

customer_behaviour.to_csv(
    customer_output,
    index=False
)

behaviour_summary.to_csv(
    summary_output,
    index=False
)

# ---------------------------------------------------------
# SUCCESS MESSAGE
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("Customer Purchase Behaviour Analysis completed successfully.")
print(f"Customer output saved to: {customer_output}")
print(f"Summary output saved to: {summary_output}")
print("=" * 70)