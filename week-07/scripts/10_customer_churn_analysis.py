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
# ANALYSIS DATE
# ---------------------------------------------------------
analysis_date = sales_orders["order_date"].max()

# ---------------------------------------------------------
# CUSTOMER CHURN DATA
# ---------------------------------------------------------
customer_churn = (
    sales_orders
    .groupby("customer_id")
    .agg(
        total_orders=("so_id", "count"),
        total_revenue=("total_order_value", "sum"),
        first_purchase_date=("order_date", "min"),
        last_purchase_date=("order_date", "max")
    )
    .reset_index()
)

# ---------------------------------------------------------
# DAYS SINCE LAST PURCHASE
# ---------------------------------------------------------
customer_churn["days_since_last_purchase"] = (
    analysis_date
    - customer_churn["last_purchase_date"]
).dt.days

# ---------------------------------------------------------
# CHURN STATUS
# ---------------------------------------------------------
def classify_churn(days):
    if days >= 365:
        return "High Churn Risk"
    elif days >= 180:
        return "Churned"
    elif days >= 90:
        return "At Risk"
    else:
        return "Active"


customer_churn["churn_status"] = (
    customer_churn["days_since_last_purchase"]
    .apply(classify_churn)
)

# ---------------------------------------------------------
# CHURN FLAG
# ---------------------------------------------------------
customer_churn["is_churned"] = (
    customer_churn["days_since_last_purchase"] >= 180
)

# ---------------------------------------------------------
# ROUND REVENUE
# ---------------------------------------------------------
customer_churn["total_revenue"] = (
    customer_churn["total_revenue"]
    .round(2)
)

# ---------------------------------------------------------
# SORT BY CHURN RISK
# ---------------------------------------------------------
customer_churn = customer_churn.sort_values(
    by="days_since_last_purchase",
    ascending=False
)

# ---------------------------------------------------------
# CHURN SUMMARY
# ---------------------------------------------------------
total_customers = len(customer_churn)

churned_customers = (
    customer_churn["is_churned"].sum()
)

churn_rate = (
    churned_customers
    / total_customers
    * 100
)

churn_summary = (
    customer_churn
    .groupby("churn_status")
    .agg(
        customers=("customer_id", "nunique"),
        total_revenue=("total_revenue", "sum"),
        average_days_since_purchase=(
            "days_since_last_purchase",
            "mean"
        )
    )
    .reset_index()
)

churn_summary["total_revenue"] = (
    churn_summary["total_revenue"].round(2)
)

churn_summary["average_days_since_purchase"] = (
    churn_summary["average_days_since_purchase"].round(2)
)

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("CUSTOMER CHURN ANALYSIS")
print("=" * 70)

print("\nCustomer Churn Analysis:")
print(
    customer_churn.head(20).to_string(index=False)
)

print("\nChurn Rate:")
print(f"{round(churn_rate, 2)}%")

print("\nChurn Summary:")
print(
    churn_summary.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------------
customer_output = (
    OUTPUT_DIR / "customer_churn_analysis.csv"
)

summary_output = (
    OUTPUT_DIR / "customer_churn_summary.csv"
)

customer_churn.to_csv(
    customer_output,
    index=False
)

churn_summary.to_csv(
    summary_output,
    index=False
)

# ---------------------------------------------------------
# SUCCESS MESSAGE
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("Customer Churn Analysis completed successfully.")
print(f"Customer output saved to: {customer_output}")
print(f"Summary output saved to: {summary_output}")
print("=" * 70)