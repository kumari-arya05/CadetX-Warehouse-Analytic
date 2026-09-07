import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Scenario-Based Inventory Forecasting
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

# Load required data
inventory = pd.read_csv(
    DATA_DIR / "inventory_master.csv"
)

demand = pd.read_csv(
    OUTPUT_DIR / "product_demand_forecasting.csv"
)

products = pd.read_csv(
    DATA_DIR / "products.csv"
)

# --------------------------------------------------
# Select required columns
# --------------------------------------------------

inventory = inventory[[
    "product_id",
    "branch_id",
    "current_stock"
]]

products = products[[
    "product_id",
    "lead_time_days",
    "safety_stock",
    "max_stock_level"
]]

# --------------------------------------------------
# Get latest demand information
# --------------------------------------------------

demand["order_date"] = pd.to_datetime(
    demand["order_date"],
    errors="coerce"
)

latest_demand = (
    demand
    .dropna(subset=["order_date"])
    .sort_values("order_date")
    .groupby("product_id")
    .tail(1)
)

latest_demand = latest_demand[[
    "product_id",
    "7_day_avg_demand",
    "30_day_avg_demand",
    "next_day_forecast"
]]

# --------------------------------------------------
# Merge datasets
# --------------------------------------------------

scenario_data = inventory.merge(
    products,
    on="product_id",
    how="left"
)

scenario_data = scenario_data.merge(
    latest_demand,
    on="product_id",
    how="left"
)

# Fill missing values
scenario_data["7_day_avg_demand"] = (
    scenario_data["7_day_avg_demand"]
    .fillna(0)
)

scenario_data["30_day_avg_demand"] = (
    scenario_data["30_day_avg_demand"]
    .fillna(0)
)

scenario_data["next_day_forecast"] = (
    scenario_data["next_day_forecast"]
    .fillna(0)
)

# --------------------------------------------------
# Base daily demand
# --------------------------------------------------

scenario_data["base_daily_demand"] = (
    scenario_data["next_day_forecast"]
)

# --------------------------------------------------
# Scenario 1: Base Demand
# --------------------------------------------------

scenario_data["base_30_day_forecast"] = (
    scenario_data["base_daily_demand"] * 30
)

scenario_data["base_60_day_forecast"] = (
    scenario_data["base_daily_demand"] * 60
)

# --------------------------------------------------
# Scenario 2: Demand Increase (+20%)
# --------------------------------------------------

scenario_data["high_demand_30_day_forecast"] = (
    scenario_data["base_daily_demand"]
    * 1.20
    * 30
)

scenario_data["high_demand_60_day_forecast"] = (
    scenario_data["base_daily_demand"]
    * 1.20
    * 60
)

# --------------------------------------------------
# Scenario 3: Demand Decrease (-20%)
# --------------------------------------------------

scenario_data["low_demand_30_day_forecast"] = (
    scenario_data["base_daily_demand"]
    * 0.80
    * 30
)

scenario_data["low_demand_60_day_forecast"] = (
    scenario_data["base_daily_demand"]
    * 0.80
    * 60
)

# --------------------------------------------------
# Estimated stock after 30 days
# --------------------------------------------------

scenario_data["base_stock_after_30_days"] = (
    scenario_data["current_stock"]
    - scenario_data["base_30_day_forecast"]
)

scenario_data["high_demand_stock_after_30_days"] = (
    scenario_data["current_stock"]
    - scenario_data["high_demand_30_day_forecast"]
)

scenario_data["low_demand_stock_after_30_days"] = (
    scenario_data["current_stock"]
    - scenario_data["low_demand_30_day_forecast"]
)

# --------------------------------------------------
# Stock status under scenarios
# --------------------------------------------------

def classify_stock(row):

    # Highest priority: stockout under high demand
    if row["high_demand_stock_after_30_days"] <= 0:
        return "High Stockout Risk"

    # Base scenario reaches safety stock
    elif row["base_stock_after_30_days"] <= row["safety_stock"]:
        return "Monitor Closely"

    # Base scenario remains above maximum stock level
    elif row["base_stock_after_30_days"] > row["max_stock_level"]:
        return "Potential Overstock"

    # Otherwise inventory position is healthy
    else:
        return "Healthy"


scenario_data["scenario_stock_status"] = (
    scenario_data.apply(
        classify_stock,
        axis=1
    )
)

# --------------------------------------------------
# Round numeric values
# --------------------------------------------------

numeric_columns = [
    "base_daily_demand",
    "base_30_day_forecast",
    "base_60_day_forecast",
    "high_demand_30_day_forecast",
    "high_demand_60_day_forecast",
    "low_demand_30_day_forecast",
    "low_demand_60_day_forecast",
    "base_stock_after_30_days",
    "high_demand_stock_after_30_days",
    "low_demand_stock_after_30_days"
]

scenario_data[numeric_columns] = (
    scenario_data[numeric_columns].round(2)
)

# --------------------------------------------------
# Save output
# --------------------------------------------------

output_file = (
    OUTPUT_DIR / "scenario_inventory_forecasting.csv"
)

scenario_data.to_csv(
    output_file,
    index=False
)

print(
    "Scenario-Based Inventory Forecasting completed successfully."
)

print(
    f"Output saved to: {output_file}"
)

print(
    f"Records generated: {len(scenario_data)}"
)