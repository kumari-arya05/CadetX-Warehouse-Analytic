import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Reorder Point Optimisation
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

# Load product and demand data
products = pd.read_csv(
    DATA_DIR / "products.csv"
)

demand = pd.read_csv(
    OUTPUT_DIR / "product_demand_forecasting.csv"
)

# Select required product information
products = products[[
    "product_id",
    "reorder_level",
    "safety_stock",
    "lead_time_days",
    "criticality_level"
]]

# Convert date
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

# Merge product and demand information
reorder_data = products.merge(
    latest_demand,
    on="product_id",
    how="left"
)

# Fill missing demand values
reorder_data["7_day_avg_demand"] = (
    reorder_data["7_day_avg_demand"]
    .fillna(0)
)

reorder_data["30_day_avg_demand"] = (
    reorder_data["30_day_avg_demand"]
    .fillna(0)
)

reorder_data["next_day_forecast"] = (
    reorder_data["next_day_forecast"]
    .fillna(0)
)

# --------------------------------------------------
# Use forecasted daily demand for planning
# --------------------------------------------------

reorder_data["average_daily_demand"] = (
    reorder_data["next_day_forecast"]
)

# Calculate demand during supplier lead time
reorder_data["lead_time_demand"] = (
    reorder_data["average_daily_demand"]
    * reorder_data["lead_time_days"]
)

# --------------------------------------------------
# Optimised reorder point
# --------------------------------------------------

reorder_data["optimised_reorder_point"] = (
    reorder_data["lead_time_demand"]
    + reorder_data["safety_stock"]
)

# Compare existing and optimised reorder levels
reorder_data["reorder_point_difference"] = (
    reorder_data["optimised_reorder_point"]
    - reorder_data["reorder_level"]
)

# --------------------------------------------------
# Classify recommendation
# --------------------------------------------------

def classify_reorder(row):

    if row["optimised_reorder_point"] > row["reorder_level"]:
        return "Increase Reorder Level"

    elif row["optimised_reorder_point"] < row["reorder_level"]:
        return "Decrease Reorder Level"

    else:
        return "Maintain Reorder Level"


reorder_data["reorder_recommendation"] = (
    reorder_data.apply(
        classify_reorder,
        axis=1
    )
)

# Round numeric values
reorder_data["average_daily_demand"] = (
    reorder_data["average_daily_demand"].round(2)
)

reorder_data["lead_time_demand"] = (
    reorder_data["lead_time_demand"].round(2)
)

reorder_data["optimised_reorder_point"] = (
    reorder_data["optimised_reorder_point"].round(2)
)

reorder_data["reorder_point_difference"] = (
    reorder_data["reorder_point_difference"].round(2)
)

# Save output
output_file = (
    OUTPUT_DIR / "reorder_point_optimization.csv"
)

reorder_data.to_csv(
    output_file,
    index=False
)

print(
    "Reorder Point Optimisation completed successfully."
)
print(
    f"Output saved to: {output_file}"
)
print(
    f"Records generated: {len(reorder_data)}"
)