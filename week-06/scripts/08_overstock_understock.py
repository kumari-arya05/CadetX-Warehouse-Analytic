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

# Convert stock columns to numeric
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
stock_analysis = inventory[
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

# ---------------------------------------------------------
# Calculate stock gaps
# ---------------------------------------------------------

stock_analysis["reorder_gap"] = (
    stock_analysis["reorder_level"]
    - stock_analysis["current_stock"]
)

stock_analysis["safety_stock_gap"] = (
    stock_analysis["safety_stock"]
    - stock_analysis["current_stock"]
)

stock_analysis["overstock_quantity"] = (
    stock_analysis["current_stock"]
    - stock_analysis["max_stock"]
)

# ---------------------------------------------------------
# Overstock / Understock classification
# ---------------------------------------------------------

def classify_stock(row):

    current = row["current_stock"]
    reorder = row["reorder_level"]
    maximum = row["max_stock"]

    if current > maximum:
        return "Overstock"

    elif current < reorder:
        return "Understock"

    else:
        return "Optimal Stock"


stock_analysis["stock_status"] = (
    stock_analysis.apply(
        classify_stock,
        axis=1
    )
)

# ---------------------------------------------------------
# Risk classification
# ---------------------------------------------------------

def risk_category(status):

    if status == "Understock":
        return "High Risk"

    elif status == "Overstock":
        return "Medium Risk"

    else:
        return "Low Risk"


stock_analysis["risk_level"] = (
    stock_analysis["stock_status"]
    .apply(risk_category)
)

# ---------------------------------------------------------
# Recommended action
# ---------------------------------------------------------

def recommended_action(row):

    if row["stock_status"] == "Understock":
        return "Reorder Stock"

    elif row["stock_status"] == "Overstock":
        return "Reduce Inventory"

    else:
        return "Maintain Stock"


stock_analysis["recommended_action"] = (
    stock_analysis.apply(
        recommended_action,
        axis=1
    )
)

# ---------------------------------------------------------
# Stock utilisation percentage
# ---------------------------------------------------------

stock_analysis["stock_utilisation_pct"] = (
    stock_analysis["current_stock"]
    / stock_analysis["max_stock"].replace(0, pd.NA)
    * 100
)

stock_analysis["stock_utilisation_pct"] = (
    stock_analysis["stock_utilisation_pct"]
    .fillna(0)
    .round(2)
)

# ---------------------------------------------------------
# Sort by risk
# ---------------------------------------------------------

risk_order = {
    "High Risk": 1,
    "Medium Risk": 2,
    "Low Risk": 3
}

stock_analysis["risk_rank"] = (
    stock_analysis["risk_level"]
    .map(risk_order)
)

stock_analysis = stock_analysis.sort_values(
    by=["risk_rank", "current_stock"],
    ascending=[True, True]
)

# ---------------------------------------------------------
# Save output
# ---------------------------------------------------------

output_file = (
    FEATURE_DIR /
    "overstock_understock.csv"
)

stock_analysis.to_csv(
    output_file,
    index=False
)

# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print(
    "\nOverstock & Understock Analysis completed successfully."
)

print(
    f"Output saved to: {output_file}"
)

print(
    f"Total inventory records analysed: "
    f"{len(stock_analysis)}"
)

print("\nStock Status Summary:")

print(
    stock_analysis["stock_status"]
    .value_counts()
)

print("\nRisk Level Summary:")

print(
    stock_analysis["risk_level"]
    .value_counts()
)

print("\nTop Risk Records:")

print(
    stock_analysis[
        [
            "product_id",
            "branch_id",
            "current_stock",
            "reorder_level",
            "max_stock",
            "stock_status",
            "risk_level",
            "recommended_action"
        ]
    ].head(10)
)