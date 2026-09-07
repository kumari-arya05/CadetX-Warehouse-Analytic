import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Week 08 Predictive Analytics Summary
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

# Load Week-08 outputs
demand = pd.read_csv(
    OUTPUT_DIR / "product_demand_forecasting.csv"
)

inventory = pd.read_csv(
    OUTPUT_DIR / "inventory_level_forecasting.csv"
)

stockout = pd.read_csv(
    OUTPUT_DIR / "stockout_risk_prediction.csv"
)

reorder = pd.read_csv(
    OUTPUT_DIR / "reorder_point_optimization.csv"
)

safety = pd.read_csv(
    OUTPUT_DIR / "safety_stock_calculation.csv"
)

scenario = pd.read_csv(
    OUTPUT_DIR / "scenario_inventory_forecasting.csv"
)

# --------------------------------------------------
# Create summary metrics
# --------------------------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Demand Forecast Records",
        "Inventory Forecast Records",
        "Stockout Risk Records",
        "Reorder Point Records",
        "Safety Stock Records",
        "Scenario Forecast Records",
        "Unique Products Analysed",

        "Critical Stockout Risk Items",
        "High Stockout Risk Items",
        "Medium Stockout Risk Items",
        "Low Stockout Risk Items",

        "Increase Reorder Level Recommendations",
        "Decrease Reorder Level Recommendations",
        "Maintain Reorder Level Recommendations",

        "Increase Safety Stock Recommendations",
        "Decrease Safety Stock Recommendations",
        "Maintain Safety Stock Recommendations",

        "High Stockout Scenario Items",
        "Monitor Closely Scenario Items",
        "Potential Overstock Scenario Items",
        "Healthy Scenario Items"
    ],

    "Value": [
        len(demand),
        len(inventory),
        len(stockout),
        len(reorder),
        len(safety),
        len(scenario),
        demand["product_id"].nunique(),

        (stockout["stockout_risk"] == "Critical").sum(),
        (stockout["stockout_risk"] == "High").sum(),
        (stockout["stockout_risk"] == "Medium").sum(),
        (stockout["stockout_risk"] == "Low").sum(),

        (reorder["reorder_recommendation"] == "Increase Reorder Level").sum(),
        (reorder["reorder_recommendation"] == "Decrease Reorder Level").sum(),
        (reorder["reorder_recommendation"] == "Maintain Reorder Level").sum(),

        (safety["safety_stock_recommendation"] == "Increase Safety Stock").sum(),
        (safety["safety_stock_recommendation"] == "Decrease Safety Stock").sum(),
        (safety["safety_stock_recommendation"] == "Maintain Safety Stock").sum(),

        (scenario["scenario_stock_status"] == "High Stockout Risk").sum(),
        (scenario["scenario_stock_status"] == "Monitor Closely").sum(),
        (scenario["scenario_stock_status"] == "Potential Overstock").sum(),
        (scenario["scenario_stock_status"] == "Healthy").sum()
    ]
})

# --------------------------------------------------
# Save summary
# --------------------------------------------------

output_file = (
    OUTPUT_DIR / "week08_predictive_analytics_summary.csv"
)

summary.to_csv(
    output_file,
    index=False
)

print(
    "Week 08 Predictive Analytics Summary completed successfully."
)

print(
    f"Output saved to: {output_file}"
)

print(
    f"Summary metrics generated: {len(summary)}"
)