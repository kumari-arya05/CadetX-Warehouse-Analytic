import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Safety Stock Calculation
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

# Load demand and product data
demand = pd.read_csv(
    OUTPUT_DIR / "product_demand_forecasting.csv"
)

products = pd.read_csv(
    DATA_DIR / "products.csv"
)

# Select required columns
products = products[[
    "product_id",
    "safety_stock",
    "lead_time_days",
    "criticality_level"
]]

# Calculate demand variability for each product
demand_variability = (
    demand
    .groupby("product_id")["quantity"]
    .agg(
        average_demand="mean",
        demand_std="std"
    )
    .reset_index()
)

# Merge product information
safety_stock_data = products.merge(
    demand_variability,
    on="product_id",
    how="left"
)

# Replace missing standard deviation
safety_stock_data["demand_std"] = (
    safety_stock_data["demand_std"].fillna(0)
)

# Service-level factor based on criticality
def get_service_factor(level):
    if level == "High":
        return 2.33
    elif level == "Medium":
        return 1.65
    else:
        return 1.28

safety_stock_data["service_factor"] = (
    safety_stock_data["criticality_level"]
    .apply(get_service_factor)
)

# Calculate recommended safety stock
safety_stock_data["recommended_safety_stock"] = (
    safety_stock_data["service_factor"]
    * safety_stock_data["demand_std"]
    * (
        safety_stock_data["lead_time_days"] ** 0.5
    )
)

# Round recommended value
safety_stock_data["recommended_safety_stock"] = (
    safety_stock_data["recommended_safety_stock"]
    .round(2)
)

# Compare existing and recommended safety stock
safety_stock_data["safety_stock_difference"] = (
    safety_stock_data["recommended_safety_stock"]
    - safety_stock_data["safety_stock"]
)

# Recommendation
def classify_safety_stock(row):
    if row["recommended_safety_stock"] > row["safety_stock"]:
        return "Increase Safety Stock"
    elif row["recommended_safety_stock"] < row["safety_stock"]:
        return "Decrease Safety Stock"
    else:
        return "Maintain Safety Stock"

safety_stock_data["safety_stock_recommendation"] = (
    safety_stock_data.apply(
        classify_safety_stock,
        axis=1
    )
)

# Save output
output_file = (
    OUTPUT_DIR / "safety_stock_calculation.csv"
)

safety_stock_data.to_csv(
    output_file,
    index=False
)

print("Safety Stock Calculation completed successfully.")
print(f"Output saved to: {output_file}")
print(f"Records generated: {len(safety_stock_data)}")