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
# LOAD SALES DATA
# ---------------------------------------------------------
sales_orders = pd.read_csv(
    DATA_DIR / "sales_orders_header.csv"
)

sales_orders["order_date"] = pd.to_datetime(
    sales_orders["order_date"],
    errors="coerce"
)

sales_orders = sales_orders.dropna(
    subset=["customer_id", "order_date"]
)

# ---------------------------------------------------------
# CUSTOMER RETENTION DATA
# ---------------------------------------------------------
customer_retention = (
    sales_orders
    .groupby("customer_id")
    .agg(
        total_orders=("so_id", "count"),
        first_purchase_date=("order_date", "min"),
        last_purchase_date=("order_date", "max"),
        total_revenue=("total_order_value", "sum")
    )
    .reset_index()
)

# ---------------------------------------------------------
# RETENTION STATUS
# ---------------------------------------------------------
customer_retention["retention_status"] = "One-Time Customer"

customer_retention.loc[
    customer_retention["total_orders"] >= 2,
    "retention_status"
] = "Retained Customer"

# ---------------------------------------------------------
# RETENTION FLAG
# ---------------------------------------------------------
customer_retention["is_retained"] = (
    customer_retention["total_orders"] >= 2
)

# ---------------------------------------------------------
# CUSTOMER LIFETIME DAYS
# ---------------------------------------------------------
customer_retention["customer_lifetime_days"] = (
    customer_retention["last_purchase_date"]
    - customer_retention["first_purchase_date"]
).dt.days

# ---------------------------------------------------------
# ROUND VALUES
# ---------------------------------------------------------
customer_retention["total_revenue"] = (
    customer_retention["total_revenue"].round(2)
)

# ---------------------------------------------------------
# SORT RESULTS
# ---------------------------------------------------------
customer_retention = customer_retention.sort_values(
    by="total_orders",
    ascending=False
)

# ---------------------------------------------------------
# RETENTION SUMMARY
# ---------------------------------------------------------
total_customers = len(customer_retention)

retained_customers = (
    customer_retention["is_retained"].sum()
)

one_time_customers = (
    total_customers - retained_customers
)

retention_rate = (
    retained_customers / total_customers * 100
)

retention_summary = pd.DataFrame({
    "metric": [
        "Total Customers",
        "Retained Customers",
        "One-Time Customers",
        "Retention Rate"
    ],
    "value": [
        total_customers,
        int(retained_customers),
        int(one_time_customers),
        round(retention_rate, 2)
    ]
})

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("CUSTOMER RETENTION ANALYSIS")
print("=" * 70)

print("\nCustomer Retention:")
print(
    customer_retention.head(20).to_string(index=False)
)

print("\nRetention Summary:")
print(
    retention_summary.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------------
customer_output = (
    OUTPUT_DIR / "customer_retention_analysis.csv"
)

summary_output = (
    OUTPUT_DIR / "customer_retention_summary.csv"
)

customer_retention.to_csv(
    customer_output,
    index=False
)

retention_summary.to_csv(
    summary_output,
    index=False
)

# ---------------------------------------------------------
# SUCCESS MESSAGE
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("Customer Retention Analysis completed successfully.")
print(f"Customer output saved to: {customer_output}")
print(f"Summary output saved to: {summary_output}")
print("=" * 70)