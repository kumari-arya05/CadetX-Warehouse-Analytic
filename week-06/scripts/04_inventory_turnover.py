import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
FEATURE_DIR = BASE_DIR / "week-06" / "data" / "features"

FEATURE_DIR.mkdir(parents=True, exist_ok=True)

# Load inventory and sales data
inventory = pd.read_csv(DATA_DIR / "inventory_master.csv")
sales_lines = pd.read_csv(DATA_DIR / "sales_orders_lines.csv")

# Clean column names
inventory.columns = inventory.columns.str.strip()
sales_lines.columns = sales_lines.columns.str.strip()

# Convert numeric columns
inventory["current_stock"] = pd.to_numeric(
    inventory["current_stock"],
    errors="coerce"
).fillna(0)

sales_lines["quantity"] = pd.to_numeric(
    sales_lines["quantity"],
    errors="coerce"
).fillna(0)

# Total quantity sold per product
sales = (
    sales_lines
    .groupby("product_id")
    .agg(
        total_quantity_sold=("quantity", "sum")
    )
    .reset_index()
)

# Inventory by product
inventory_product = (
    inventory
    .groupby("product_id")
    .agg(
        average_inventory=("current_stock", "mean"),
        total_inventory=("current_stock", "sum")
    )
    .reset_index()
)

# Merge sales and inventory
turnover = inventory_product.merge(
    sales,
    on="product_id",
    how="left"
)

turnover["total_quantity_sold"] = (
    turnover["total_quantity_sold"].fillna(0)
)

# Inventory turnover ratio
turnover["inventory_turnover_ratio"] = (
    turnover["total_quantity_sold"]
    / turnover["average_inventory"].replace(0, pd.NA)
)

turnover["inventory_turnover_ratio"] = (
    turnover["inventory_turnover_ratio"]
    .fillna(0)
    .round(2)
)

# Turnover category
def turnover_category(ratio):
    if ratio >= 5:
        return "High Turnover"
    elif ratio >= 2:
        return "Medium Turnover"
    elif ratio > 0:
        return "Low Turnover"
    else:
        return "No Turnover"

turnover["turnover_category"] = (
    turnover["inventory_turnover_ratio"]
    .apply(turnover_category)
)

# Ranking
turnover["turnover_rank"] = (
    turnover["inventory_turnover_ratio"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)

# Sort
turnover = turnover.sort_values(
    by="inventory_turnover_ratio",
    ascending=False
)

# Save output
output_file = FEATURE_DIR / "inventory_turnover.csv"

turnover.to_csv(
    output_file,
    index=False
)

print("\nInventory Turnover Analysis completed successfully.")
print(f"Output saved to: {output_file}")
print(f"Total products analysed: {len(turnover)}")

print("\nTop 10 Inventory Turnover Products:")
print(turnover.head(10))