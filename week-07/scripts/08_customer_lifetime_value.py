import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load customer data
customers = pd.read_csv(
    DATA_DIR / "customers.csv"
)

# Load sales orders
sales_orders = pd.read_csv(
    DATA_DIR / "sales_orders_header.csv"
)

# Date conversion
sales_orders["order_date"] = pd.to_datetime(
    sales_orders["order_date"],
    errors="coerce"
)

# Remove invalid records
sales_orders = sales_orders.dropna(
    subset=["customer_id", "order_date"]
)

# ---------------------------------------------------------
# CUSTOMER REVENUE
# ---------------------------------------------------------
customer_revenue = (
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
# CUSTOMER LIFETIME
# ---------------------------------------------------------
customer_revenue["customer_lifetime_days"] = (
    customer_revenue["last_purchase_date"]
    - customer_revenue["first_purchase_date"]
).dt.days

customer_revenue["customer_lifetime_years"] = (
    customer_revenue["customer_lifetime_days"] / 365
)

# Avoid zero lifetime
customer_revenue["customer_lifetime_years"] = (
    customer_revenue["customer_lifetime_years"]
    .replace(0, 1 / 365)
)

# ---------------------------------------------------------
# ANNUAL CUSTOMER VALUE
# ---------------------------------------------------------
customer_revenue["annual_customer_value"] = (
    customer_revenue["total_revenue"]
    / customer_revenue["customer_lifetime_years"]
)

# ---------------------------------------------------------
# ESTIMATED 3-YEAR CLV
# ---------------------------------------------------------
customer_revenue["estimated_3_year_clv"] = (
    customer_revenue["annual_customer_value"] * 3
)

# ---------------------------------------------------------
# CLV SEGMENT
# ---------------------------------------------------------
clv_threshold_high = (
    customer_revenue["estimated_3_year_clv"]
    .quantile(0.80)
)

clv_threshold_medium = (
    customer_revenue["estimated_3_year_clv"]
    .quantile(0.50)
)

def classify_clv(value):
    if value >= clv_threshold_high:
        return "High CLV"
    elif value >= clv_threshold_medium:
        return "Medium CLV"
    else:
        return "Low CLV"

customer_revenue["clv_segment"] = (
    customer_revenue["estimated_3_year_clv"]
    .apply(classify_clv)
)

# ---------------------------------------------------------
# MERGE CUSTOMER DETAILS
# ---------------------------------------------------------
customer_details = customers[
    [
        "customer_id",
        "customer_type",
        "industry_segment",
        "city",
        "state",
        "region",
        "customer_rating"
    ]
].drop_duplicates(
    subset=["customer_id"]
)

clv = customer_details.merge(
    customer_revenue,
    on="customer_id",
    how="inner"
)

# ---------------------------------------------------------
# ROUND VALUES
# ---------------------------------------------------------
for column in [
    "total_revenue",
    "customer_lifetime_years",
    "annual_customer_value",
    "estimated_3_year_clv"
]:
    clv[column] = clv[column].round(2)

# ---------------------------------------------------------
# SORT BY CLV
# ---------------------------------------------------------
clv = clv.sort_values(
    by="estimated_3_year_clv",
    ascending=False
)

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("CUSTOMER LIFETIME VALUE ANALYSIS")
print("=" * 70)

print("\nCustomer Lifetime Value:")

print(
    clv.head(20).to_string(index=False)
)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------
clv_summary = (
    clv
    .groupby("clv_segment")
    .agg(
        customers=("customer_id", "nunique"),
        total_revenue=("total_revenue", "sum"),
        average_clv=("estimated_3_year_clv", "mean"),
        total_clv=("estimated_3_year_clv", "sum")
    )
    .reset_index()
)

clv_summary["total_revenue"] = (
    clv_summary["total_revenue"].round(2)
)

clv_summary["average_clv"] = (
    clv_summary["average_clv"].round(2)
)

clv_summary["total_clv"] = (
    clv_summary["total_clv"].round(2)
)

print("\nCLV Segment Summary:")

print(
    clv_summary.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------------
clv_output = (
    OUTPUT_DIR / "customer_lifetime_value.csv"
)

summary_output = (
    OUTPUT_DIR / "customer_lifetime_value_summary.csv"
)

clv.to_csv(
    clv_output,
    index=False
)

clv_summary.to_csv(
    summary_output,
    index=False
)

print("\n" + "=" * 70)
print("Customer Lifetime Value Analysis completed successfully.")
print(f"CLV output saved to: {clv_output}")
print(f"Summary output saved to: {summary_output}")
print("=" * 70)