import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Product Demand Forecasting
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

# Load datasets
sales_lines = pd.read_csv(
    DATA_DIR / "sales_orders_lines.csv"
)

sales_header = pd.read_csv(
    DATA_DIR / "sales_orders_header.csv"
)

# Select required columns
sales_lines = sales_lines[[
    "so_id",
    "product_id",
    "quantity"
]]

sales_header = sales_header[[
    "so_id",
    "order_date"
]]

# Merge sales lines with order dates
sales_data = sales_lines.merge(
    sales_header,
    on="so_id",
    how="left"
)

# Convert date column
sales_data["order_date"] = pd.to_datetime(
    sales_data["order_date"],
    errors="coerce"
)

# Remove invalid records
sales_data = sales_data.dropna(
    subset=["order_date", "product_id", "quantity"]
)

# Aggregate demand by product and calendar date
daily_demand = (
    sales_data
    .groupby(
        ["product_id", "order_date"],
        as_index=False
    )["quantity"]
    .sum()
)

# --------------------------------------------------
# Create complete calendar for each product
# --------------------------------------------------

product_dates = []

for product_id, group in daily_demand.groupby("product_id"):
    date_range = pd.date_range(
        start=group["order_date"].min(),
        end=group["order_date"].max(),
        freq="D"
    )

    temp = pd.DataFrame({
        "product_id": product_id,
        "order_date": date_range
    })

    product_dates.append(temp)

calendar_demand = pd.concat(
    product_dates,
    ignore_index=True
)

# Merge actual demand into complete calendar
daily_demand = calendar_demand.merge(
    daily_demand,
    on=["product_id", "order_date"],
    how="left"
)

# No sales on a date = zero demand
daily_demand["quantity"] = (
    daily_demand["quantity"]
    .fillna(0)
)

# Sort data
daily_demand = daily_demand.sort_values(
    ["product_id", "order_date"]
)

# --------------------------------------------------
# Calculate actual calendar-day rolling averages
# --------------------------------------------------

daily_demand["7_day_avg_demand"] = (
    daily_demand
    .groupby("product_id")["quantity"]
    .transform(
        lambda x: x.rolling(
            window=7,
            min_periods=1
        ).mean()
    )
)

daily_demand["30_day_avg_demand"] = (
    daily_demand
    .groupby("product_id")["quantity"]
    .transform(
        lambda x: x.rolling(
            window=30,
            min_periods=1
        ).mean()
    )
)

# --------------------------------------------------
# Next-day demand forecast
# --------------------------------------------------

daily_demand["next_day_forecast"] = (
    daily_demand["7_day_avg_demand"]
)

# Round forecast values
daily_demand["7_day_avg_demand"] = (
    daily_demand["7_day_avg_demand"].round(2)
)

daily_demand["30_day_avg_demand"] = (
    daily_demand["30_day_avg_demand"].round(2)
)

daily_demand["next_day_forecast"] = (
    daily_demand["next_day_forecast"].round(2)
)

# Save output
output_file = (
    OUTPUT_DIR / "product_demand_forecasting.csv"
)

daily_demand.to_csv(
    output_file,
    index=False
)

print(
    "Product Demand Forecasting completed successfully."
)
print(f"Output saved to: {output_file}")
print(
    f"Records generated: {len(daily_demand)}"
)