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

# Convert numeric columns
sales_lines["quantity"] = pd.to_numeric(
    sales_lines["quantity"],
    errors="coerce"
).fillna(0)

sales_lines["line_total"] = pd.to_numeric(
    sales_lines["line_total"],
    errors="coerce"
).fillna(0)

# ---------------------------------------------------------
# Calculate product sales value
# ---------------------------------------------------------

product_sales = (
    sales_lines
    .groupby("product_id")
    .agg(
        total_quantity_sold=("quantity", "sum"),
        total_sales_value=("line_total", "sum")
    )
    .reset_index()
)

# ---------------------------------------------------------
# Sort products by sales value
# ---------------------------------------------------------

product_sales = product_sales.sort_values(
    by="total_sales_value",
    ascending=False
).reset_index(drop=True)

# ---------------------------------------------------------
# Calculate sales contribution
# ---------------------------------------------------------

total_sales = product_sales["total_sales_value"].sum()

if total_sales > 0:
    product_sales["sales_contribution_pct"] = (
        product_sales["total_sales_value"]
        / total_sales
        * 100
    )
else:
    product_sales["sales_contribution_pct"] = 0

product_sales["sales_contribution_pct"] = (
    product_sales["sales_contribution_pct"]
    .round(2)
)

# ---------------------------------------------------------
# Calculate cumulative contribution
# ---------------------------------------------------------

product_sales["cumulative_contribution_pct"] = (
    product_sales["sales_contribution_pct"]
    .cumsum()
    .round(2)
)

# ---------------------------------------------------------
# ABC classification
# ---------------------------------------------------------

def abc_category(cumulative_pct):

    if cumulative_pct <= 80:
        return "A"

    elif cumulative_pct <= 95:
        return "B"

    else:
        return "C"


product_sales["abc_category"] = (
    product_sales["cumulative_contribution_pct"]
    .apply(abc_category)
)

# ---------------------------------------------------------
# Product ranking
# ---------------------------------------------------------

product_sales["sales_rank"] = (
    product_sales["total_sales_value"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)

# ---------------------------------------------------------
# Pareto group
# ---------------------------------------------------------

def pareto_group(category):

    if category == "A":
        return "High Value"

    elif category == "B":
        return "Medium Value"

    else:
        return "Low Value"


product_sales["pareto_group"] = (
    product_sales["abc_category"]
    .apply(pareto_group)
)

# ---------------------------------------------------------
# Sort by rank
# ---------------------------------------------------------

product_sales = product_sales.sort_values(
    by="sales_rank",
    ascending=True
)

# ---------------------------------------------------------
# Save output
# ---------------------------------------------------------

output_file = (
    FEATURE_DIR / "abc_pareto_products.csv"
)

product_sales.to_csv(
    output_file,
    index=False
)

# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print(
    "\nABC / Pareto Product Classification completed successfully."
)

print(
    f"Output saved to: {output_file}"
)

print(
    f"Total products analysed: "
    f"{len(product_sales)}"
)

print("\nABC Category Summary:")

print(
    product_sales["abc_category"]
    .value_counts()
    .sort_index()
)

print("\nTop 10 Products:")

print(
    product_sales.head(10)
)