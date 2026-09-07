import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Stockout Risk Prediction
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

# Load inventory, product and demand data
inventory = pd.read_csv(
    DATA_DIR / "inventory_master.csv"
)

products = pd.read_csv(
    DATA_DIR / "products.csv"
)

demand = pd.read_csv(
    OUTPUT_DIR / "product_demand_forecasting.csv"
)

# --------------------------------------------------
# Select required columns
# --------------------------------------------------

inventory = inventory[[
    "product_id",
    "branch_id",
    "current_stock",
    "reorder_level",
    "safety_stock"
]]

products = products[[
    "product_id",
    "lead_time_days",
    "criticality_level",
    "usage_frequency"
]]

demand["order_date"] = pd.to_datetime(
    demand["order_date"],
    errors="coerce"
)

# Get latest demand forecast for each product
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
# Merge inventory and product information
# --------------------------------------------------

risk_data = inventory.merge(
    products,
    on="product_id",
    how="left"
)

risk_data = risk_data.merge(
    latest_demand,
    on="product_id",
    how="left"
)

# Fill missing values
risk_data["lead_time_days"] = (
    risk_data["lead_time_days"]
    .fillna(0)
)

risk_data["7_day_avg_demand"] = (
    risk_data["7_day_avg_demand"]
    .fillna(0)
)

risk_data["30_day_avg_demand"] = (
    risk_data["30_day_avg_demand"]
    .fillna(0)
)

risk_data["next_day_forecast"] = (
    risk_data["next_day_forecast"]
    .fillna(0)
)

# --------------------------------------------------
# Calculate stock gaps
# --------------------------------------------------

risk_data["stock_gap"] = (
    risk_data["current_stock"]
    - risk_data["reorder_level"]
)

risk_data["safety_stock_gap"] = (
    risk_data["current_stock"]
    - risk_data["safety_stock"]
)

# --------------------------------------------------
# Estimate demand during supplier lead time
# --------------------------------------------------

risk_data["lead_time_demand"] = (
    risk_data["next_day_forecast"]
    * risk_data["lead_time_days"]
)

# Project stock at the end of lead time
risk_data["projected_stock_after_lead_time"] = (
    risk_data["current_stock"]
    - risk_data["lead_time_demand"]
)

# --------------------------------------------------
# Define stockout risk
# --------------------------------------------------

def calculate_risk(row):

    if row["current_stock"] <= 0:
        return "Critical"

    elif row["projected_stock_after_lead_time"] <= 0:
        return "High"

    elif row["projected_stock_after_lead_time"] <= row["safety_stock"]:
        return "Medium"

    elif row["projected_stock_after_lead_time"] <= row["reorder_level"]:
        return "Low"

    else:
        return "Low"


risk_data["stockout_risk"] = (
    risk_data.apply(
        calculate_risk,
        axis=1
    )
)

# --------------------------------------------------
# Risk score
# --------------------------------------------------

risk_data["stockout_risk_score"] = (
    risk_data["projected_stock_after_lead_time"]
    / risk_data["reorder_level"].replace(0, 1)
)

risk_data["stockout_risk_score"] = (
    risk_data["stockout_risk_score"]
    .round(2)
)

# --------------------------------------------------
# Save output
# --------------------------------------------------

output_file = (
    OUTPUT_DIR / "stockout_risk_prediction.csv"
)

risk_data.to_csv(
    output_file,
    index=False
)

print(
    "Stockout Risk Prediction completed successfully."
)
print(
    f"Output saved to: {output_file}"
)
print(
    f"Records generated: {len(risk_data)}"
)