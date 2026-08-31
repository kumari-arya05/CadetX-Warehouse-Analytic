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

# Calculate product sales quantity
fast_moving = (
    sales_lines
    .groupby("product_id")
    .agg(
        total_quantity_sold=("quantity", "sum"),
        sales_order_lines=("quantity", "count")
    )
    .reset_index()
)

# Calculate average quantity per order line
fast_moving["average_quantity_per_order"] = (
    fast_moving["total_quantity_sold"]
    / fast_moving["sales_order_lines"]
)

fast_moving["average_quantity_per_order"] = (
    fast_moving["average_quantity_per_order"]
    .round(2)
)

# Rank products by quantity sold
fast_moving["fast_moving_rank"] = (
    fast_moving["total_quantity_sold"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)

# Fast-moving category
def classify_product(rank):
    if rank <= 10:
        return "Fast Moving"
    elif rank <= 20:
        return "Moderate Moving"
    else:
        return "Slow Moving"

fast_moving["movement_category"] = (
    fast_moving["fast_moving_rank"]
    .apply(classify_product)
)

# Sort by quantity sold
fast_moving = fast_moving.sort_values(
    by="total_quantity_sold",
    ascending=False
)

# Save output
output_file = (
    FEATURE_DIR / "fast_moving_products.csv"
)

fast_moving.to_csv(
    output_file,
    index=False
)

# Display results
print("\nFast-Moving Product Analysis completed successfully.")

print(f"Output saved to: {output_file}")

print(
    f"Total products analysed: "
    f"{len(fast_moving)}"
)

print("\nTop 10 Fast-Moving Products:")
print(fast_moving.head(10))