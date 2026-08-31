import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
FEATURE_DIR = BASE_DIR / "week-06" / "data" / "features"

FEATURE_DIR.mkdir(parents=True, exist_ok=True)

# Load sales data
sales_lines = pd.read_csv(
    DATA_DIR / "sales_orders_lines.csv"
)

sales_header = pd.read_csv(
    DATA_DIR / "sales_orders_header.csv"
)

# Clean column names
sales_lines.columns = sales_lines.columns.str.strip()
sales_header.columns = sales_header.columns.str.strip()

print("Sales Header columns:")
print(sales_header.columns.tolist())

# ---------------------------------------------------------
# Find date column
# ---------------------------------------------------------

date_candidates = [
    "order_date",
    "sales_date",
    "so_date",
    "date",
    "created_at",
    "transaction_date",
    "order_datetime"
]

date_column = None

for column in date_candidates:
    if column in sales_header.columns:
        date_column = column
        break

if date_column is None:
    raise ValueError(
        "Sales date column was not found."
    )

# Convert date
sales_header[date_column] = pd.to_datetime(
    sales_header[date_column],
    errors="coerce"
)

sales_header = sales_header.dropna(
    subset=[date_column]
)

# ---------------------------------------------------------
# Find sales order ID
# ---------------------------------------------------------

order_id_candidates = [
    "so_id",
    "sales_order_id",
    "order_id"
]

order_id_column = None

for column in order_id_candidates:
    if column in sales_header.columns:
        order_id_column = column
        break

if order_id_column is None:
    raise ValueError(
        "Sales order ID column was not found."
    )

# ---------------------------------------------------------
# Convert quantity
# ---------------------------------------------------------

sales_lines["quantity"] = pd.to_numeric(
    sales_lines["quantity"],
    errors="coerce"
).fillna(0)

# ---------------------------------------------------------
# Merge sales lines with sales dates
# ---------------------------------------------------------

sales_data = sales_lines.merge(
    sales_header[
        [order_id_column, date_column]
    ],
    left_on="so_id",
    right_on=order_id_column,
    how="left"
)

sales_data = sales_data.dropna(
    subset=[date_column]
)

# ---------------------------------------------------------
# Create monthly demand
# ---------------------------------------------------------

sales_data["month"] = (
    sales_data[date_column]
    .dt.to_period("M")
    .astype(str)
)

monthly_demand = (
    sales_data
    .groupby(
        ["product_id", "month"]
    )
    .agg(
        monthly_quantity_sold=("quantity", "sum"),
        sales_order_lines=("quantity", "count")
    )
    .reset_index()
)

# ---------------------------------------------------------
# Calculate demand statistics
# ---------------------------------------------------------

demand_summary = (
    monthly_demand
    .groupby("product_id")
    .agg(
        average_monthly_demand=(
            "monthly_quantity_sold",
            "mean"
        ),
        total_demand=(
            "monthly_quantity_sold",
            "sum"
        ),
        peak_monthly_demand=(
            "monthly_quantity_sold",
            "max"
        ),
        demand_months=(
            "month",
            "count"
        )
    )
    .reset_index()
)

# ---------------------------------------------------------
# Calculate first and last month demand
# ---------------------------------------------------------

monthly_sorted = monthly_demand.sort_values(
    ["product_id", "month"]
)

first_month = (
    monthly_sorted
    .groupby("product_id")
    .first()
    .reset_index()
)

last_month = (
    monthly_sorted
    .groupby("product_id")
    .last()
    .reset_index()
)

first_month = first_month[
    [
        "product_id",
        "monthly_quantity_sold"
    ]
].rename(
    columns={
        "monthly_quantity_sold":
        "first_month_demand"
    }
)

last_month = last_month[
    [
        "product_id",
        "monthly_quantity_sold"
    ]
].rename(
    columns={
        "monthly_quantity_sold":
        "last_month_demand"
    }
)

# Merge first and last demand
demand_summary = demand_summary.merge(
    first_month,
    on="product_id",
    how="left"
)

demand_summary = demand_summary.merge(
    last_month,
    on="product_id",
    how="left"
)

# ---------------------------------------------------------
# Demand change percentage
# ---------------------------------------------------------

demand_summary["demand_change_pct"] = (
    (
        demand_summary["last_month_demand"]
        - demand_summary["first_month_demand"]
    )
    / demand_summary["first_month_demand"].replace(
        0,
        pd.NA
    )
    * 100
)

demand_summary["demand_change_pct"] = (
    demand_summary["demand_change_pct"]
    .fillna(0)
    .round(2)
)

# ---------------------------------------------------------
# Demand trend classification
# ---------------------------------------------------------

def demand_trend(change):

    if change >= 10:
        return "Increasing"

    elif change <= -10:
        return "Decreasing"

    else:
        return "Stable"


demand_summary["demand_trend"] = (
    demand_summary["demand_change_pct"]
    .apply(demand_trend)
)

# ---------------------------------------------------------
# Demand category
# ---------------------------------------------------------

def demand_category(avg_demand):

    if avg_demand >= 5000:
        return "High Demand"

    elif avg_demand >= 2500:
        return "Medium Demand"

    else:
        return "Low Demand"


demand_summary["demand_category"] = (
    demand_summary["average_monthly_demand"]
    .apply(demand_category)
)

# ---------------------------------------------------------
# Demand rank
# ---------------------------------------------------------

demand_summary["demand_rank"] = (
    demand_summary["total_demand"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)

# Round numeric columns
demand_summary[
    [
        "average_monthly_demand",
        "total_demand",
        "peak_monthly_demand"
    ]
] = demand_summary[
    [
        "average_monthly_demand",
        "total_demand",
        "peak_monthly_demand"
    ]
].round(2)

# ---------------------------------------------------------
# Sort by demand rank
# ---------------------------------------------------------

demand_summary = demand_summary.sort_values(
    by="demand_rank",
    ascending=True
)

# ---------------------------------------------------------
# Save output
# ---------------------------------------------------------

output_file = (
    FEATURE_DIR /
    "product_demand_trend.csv"
)

demand_summary.to_csv(
    output_file,
    index=False
)

# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print(
    "\nProduct Demand Trend Analysis completed successfully."
)

print(
    f"Output saved to: {output_file}"
)

print(
    f"Total products analysed: "
    f"{len(demand_summary)}"
)

print("\nDemand Trend Summary:")

print(
    demand_summary["demand_trend"]
    .value_counts()
)

print("\nDemand Category Summary:")

print(
    demand_summary["demand_category"]
    .value_counts()
)

print("\nTop 10 Products by Demand:")

print(
    demand_summary.head(10)
)