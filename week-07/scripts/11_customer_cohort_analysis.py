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
# ORDER MONTH
# ---------------------------------------------------------
sales_orders["order_month"] = (
    sales_orders["order_date"].dt.to_period("M")
)

# ---------------------------------------------------------
# FIRST PURCHASE / COHORT MONTH
# ---------------------------------------------------------
first_purchase = (
    sales_orders
    .groupby("customer_id")["order_month"]
    .min()
    .reset_index()
)

first_purchase = first_purchase.rename(
    columns={
        "order_month": "cohort_month"
    }
)

sales_orders = sales_orders.merge(
    first_purchase,
    on="customer_id",
    how="left"
)

# ---------------------------------------------------------
# COHORT INDEX
# ---------------------------------------------------------
sales_orders["cohort_index"] = (
    (
        sales_orders["order_month"].dt.year
        - sales_orders["cohort_month"].dt.year
    ) * 12
    +
    (
        sales_orders["order_month"].dt.month
        - sales_orders["cohort_month"].dt.month
    )
    + 1
)

# ---------------------------------------------------------
# COHORT CUSTOMER DATA
# ---------------------------------------------------------
cohort_data = (
    sales_orders
    .groupby(
        ["cohort_month", "cohort_index"]
    )
    .agg(
        active_customers=(
            "customer_id",
            "nunique"
        )
    )
    .reset_index()
)

# ---------------------------------------------------------
# COHORT SIZE
# ---------------------------------------------------------
cohort_sizes = (
    cohort_data[
        cohort_data["cohort_index"] == 1
    ][
        [
            "cohort_month",
            "active_customers"
        ]
    ]
    .rename(
        columns={
            "active_customers": "cohort_size"
        }
    )
)

cohort_data = cohort_data.merge(
    cohort_sizes,
    on="cohort_month",
    how="left"
)

# ---------------------------------------------------------
# RETENTION RATE
# ---------------------------------------------------------
cohort_data["retention_rate"] = (
    cohort_data["active_customers"]
    / cohort_data["cohort_size"]
    * 100
)

# ---------------------------------------------------------
# COHORT REVENUE
# ---------------------------------------------------------
cohort_revenue = (
    sales_orders
    .groupby(
        ["cohort_month", "cohort_index"]
    )
    .agg(
        revenue=(
            "total_order_value",
            "sum"
        )
    )
    .reset_index()
)

cohort_data = cohort_data.merge(
    cohort_revenue,
    on=[
        "cohort_month",
        "cohort_index"
    ],
    how="left"
)

# ---------------------------------------------------------
# ROUND VALUES
# ---------------------------------------------------------
cohort_data["retention_rate"] = (
    cohort_data["retention_rate"]
    .round(2)
)

cohort_data["revenue"] = (
    cohort_data["revenue"]
    .round(2)
)

# ---------------------------------------------------------
# RETENTION MATRIX
# ---------------------------------------------------------
retention_matrix = cohort_data.pivot(
    index="cohort_month",
    columns="cohort_index",
    values="retention_rate"
)

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("CUSTOMER COHORT ANALYSIS")
print("=" * 70)

print("\nCohort Analysis:")
print(
    cohort_data.head(20).to_string(
        index=False
    )
)

print("\nRetention Matrix:")
print(
    retention_matrix.to_string()
)

# ---------------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------------
cohort_output = (
    OUTPUT_DIR / "customer_cohort_analysis.csv"
)

matrix_output = (
    OUTPUT_DIR / "customer_cohort_retention_matrix.csv"
)

cohort_data.to_csv(
    cohort_output,
    index=False
)

retention_matrix.to_csv(
    matrix_output
)

print("\n" + "=" * 70)
print("Customer Cohort Analysis completed successfully.")
print(f"Cohort output saved to: {cohort_output}")
print(f"Retention matrix saved to: {matrix_output}")
print("=" * 70)