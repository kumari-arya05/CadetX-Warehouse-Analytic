import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
FEATURE_DIR = BASE_DIR / "week-06" / "data" / "features"

FEATURE_DIR.mkdir(parents=True, exist_ok=True)

# Load inventory data
inventory = pd.read_csv(
    DATA_DIR / "inventory_master.csv"
)

# Clean column names
inventory.columns = inventory.columns.str.strip()

print("Inventory columns:")
print(inventory.columns.tolist())

# Convert stock-related columns to numeric
stock_columns = [
    "opening_stock",
    "reorder_level",
    "safety_stock",
    "max_stock",
    "current_stock"
]

for column in stock_columns:
    inventory[column] = pd.to_numeric(
        inventory[column],
        errors="coerce"
    ).fillna(0)

# Select required columns
stock_health = inventory[
    [
        "product_id",
        "branch_id",
        "opening_stock",
        "current_stock",
        "reorder_level",
        "safety_stock",
        "max_stock",
        "warehouse_bin"
    ]
].copy()

# Calculate stock gaps
stock_health["reorder_gap"] = (
    stock_health["current_stock"]
    - stock_health["reorder_level"]
)

stock_health["safety_stock_gap"] = (
    stock_health["current_stock"]
    - stock_health["safety_stock"]
)

stock_health["max_stock_gap"] = (
    stock_health["max_stock"]
    - stock_health["current_stock"]
)

# Stock utilisation percentage
stock_health["stock_utilisation_pct"] = (
    stock_health["current_stock"]
    / stock_health["max_stock"].replace(0, pd.NA)
    * 100
)

stock_health["stock_utilisation_pct"] = (
    stock_health["stock_utilisation_pct"]
    .fillna(0)
    .round(2)
)

# Stock health classification
def classify_stock(row):

    current = row["current_stock"]
    reorder = row["reorder_level"]
    safety = row["safety_stock"]
    maximum = row["max_stock"]

    if current <= 0:
        return "Out of Stock"

    elif current < safety:
        return "Critical Low Stock"

    elif current < reorder:
        return "Low Stock"

    elif current > maximum:
        return "Overstock"

    else:
        return "Healthy Stock"


stock_health["stock_health_status"] = (
    stock_health.apply(
        classify_stock,
        axis=1
    )
)

# Risk level
def assign_risk(status):

    if status in [
        "Out of Stock",
        "Critical Low Stock"
    ]:
        return "High Risk"

    elif status in [
        "Low Stock",
        "Overstock"
    ]:
        return "Medium Risk"

    else:
        return "Low Risk"


stock_health["risk_level"] = (
    stock_health["stock_health_status"]
    .apply(assign_risk)
)

# Stock health score
def health_score(status):

    scores = {
        "Healthy Stock": 100,
        "Low Stock": 60,
        "Overstock": 50,
        "Critical Low Stock": 30,
        "Out of Stock": 0
    }

    return scores.get(status, 0)


stock_health["stock_health_score"] = (
    stock_health["stock_health_status"]
    .apply(health_score)
)

# Risk ranking
risk_order = {
    "High Risk": 1,
    "Medium Risk": 2,
    "Low Risk": 3
}

stock_health["risk_rank"] = (
    stock_health["risk_level"]
    .map(risk_order)
)

# Sort results
stock_health = stock_health.sort_values(
    by=["risk_rank", "stock_health_score"],
    ascending=[True, True]
)

# Save output
output_file = (
    FEATURE_DIR /
    "stock_health_assessment.csv"
)

stock_health.to_csv(
    output_file,
    index=False
)

# Summary
print(
    "\nStock Health Assessment completed successfully."
)

print(
    f"Output saved to: {output_file}"
)

print(
    f"Total inventory records analysed: "
    f"{len(stock_health)}"
)

print("\nStock Health Summary:")

print(
    stock_health["stock_health_status"]
    .value_counts()
)

print("\nRisk Level Summary:")

print(
    stock_health["risk_level"]
    .value_counts()
)