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

print("Sales Lines columns:")
print(sales_lines.columns.tolist())

# Convert numeric columns
numeric_columns = [
    "quantity",
    "unit_price",
    "gst_rate",
    "line_total",
    "gst_amount",
    "line_grand_total"
]

for column in numeric_columns:
    if column in sales_lines.columns:
        sales_lines[column] = pd.to_numeric(
            sales_lines[column],
            errors="coerce"
        ).fillna(0)

# Product performance analysis
product_performance = (
    sales_lines
    .groupby("product_id")
    .agg(
        total_quantity_sold=("quantity", "sum"),
        sales_order_lines=("quantity", "count"),
        total_sales_value=("line_total", "sum"),
        total_gst=("gst_amount", "sum"),
        total_grand_value=("line_grand_total", "sum"),
        average_unit_price=("unit_price", "mean")
    )
    .reset_index()
)

# Calculate average sales value per order line
product_performance["average_sales_value"] = (
    product_performance["total_sales_value"]
    / product_performance["sales_order_lines"]
)

product_performance["average_sales_value"] = (
    product_performance["average_sales_value"]
    .round(2)
)

# Calculate sales contribution percentage
total_sales = product_performance[
    "total_sales_value"
].sum()

if total_sales > 0:
    product_performance["sales_contribution_pct"] = (
        product_performance["total_sales_value"]
        / total_sales
        * 100
    )
else:
    product_performance["sales_contribution_pct"] = 0

product_performance["sales_contribution_pct"] = (
    product_performance["sales_contribution_pct"]
    .round(2)
)

# Product ranking
product_performance["performance_rank"] = (
    product_performance["total_sales_value"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)

# Performance category
def performance_category(rank):
    if rank <= 10:
        return "High Performer"
    elif rank <= 20:
        return "Medium Performer"
    else:
        return "Low Performer"

product_performance["performance_category"] = (
    product_performance["performance_rank"]
    .apply(performance_category)
)

# Sort by sales value
product_performance = product_performance.sort_values(
    by="total_sales_value",
    ascending=False
)

# Save output
output_file = (
    FEATURE_DIR / "product_performance.csv"
)

product_performance.to_csv(
    output_file,
    index=False
)

# Completion message
print(
    "\nProduct Performance Analysis completed successfully."
)

print(f"Output saved to: {output_file}")

print(
    f"Total products analysed: "
    f"{len(product_performance)}"
)

print("\nTop 10 Products:")
print(product_performance.head(10))