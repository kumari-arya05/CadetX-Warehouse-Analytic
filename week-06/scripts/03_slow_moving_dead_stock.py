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

# Clean column names
sales_lines.columns = sales_lines.columns.str.strip()

# Convert quantity to numeric
sales_lines["quantity"] = pd.to_numeric(
    sales_lines["quantity"],
    errors="coerce"
).fillna(0)

# Calculate product movement
product_sales = (
    sales_lines
    .groupby("product_id")
    .agg(
        total_quantity_sold=("quantity", "sum"),
        sales_order_lines=("quantity", "count")
    )
    .reset_index()
)

# Average quantity sold per order line
product_sales["average_quantity_per_order"] = (
    product_sales["total_quantity_sold"]
    / product_sales["sales_order_lines"]
)

product_sales["average_quantity_per_order"] = (
    product_sales["average_quantity_per_order"]
    .round(2)
)

# Rank products from lowest sales quantity
product_sales["slow_moving_rank"] = (
    product_sales["total_quantity_sold"]
    .rank(
        method="dense",
        ascending=True
    )
    .astype(int)
)

# Movement category
def movement_category(rank):
    if rank <= 10:
        return "Slow Moving"
    elif rank <= 20:
        return "Moderate Moving"
    else:
        return "Fast Moving"

product_sales["movement_category"] = (
    product_sales["slow_moving_rank"]
    .apply(movement_category)
)

# Dead stock identification
product_sales["dead_stock"] = (
    product_sales["total_quantity_sold"] == 0
)

# Risk classification
def risk_category(row):
    if row["dead_stock"]:
        return "High Risk"
    elif row["movement_category"] == "Slow Moving":
        return "Medium Risk"
    else:
        return "Low Risk"

product_sales["stock_risk"] = (
    product_sales.apply(
        risk_category,
        axis=1
    )
)

# Sort slowest products first
product_sales = product_sales.sort_values(
    by="total_quantity_sold",
    ascending=True
)

# Save output
output_file = (
    FEATURE_DIR / "slow_moving_dead_stock.csv"
)

product_sales.to_csv(
    output_file,
    index=False
)

# Display results
print("\nSlow-Moving & Dead Stock Analysis completed successfully.")

print(f"Output saved to: {output_file}")

print(
    f"Total products analysed: "
    f"{len(product_sales)}"
)

print("\nTop 10 Slow-Moving Products:")
print(product_sales.head(10))