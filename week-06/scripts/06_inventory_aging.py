import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
FEATURE_DIR = BASE_DIR / "week-06" / "data" / "features"

FEATURE_DIR.mkdir(parents=True, exist_ok=True)

# Load inventory and sales data
inventory = pd.read_csv(
    DATA_DIR / "inventory_master.csv"
)

sales_lines = pd.read_csv(
    DATA_DIR / "sales_orders_lines.csv"
)

sales_header = pd.read_csv(
    DATA_DIR / "sales_orders_header.csv"
)

# Clean column names
inventory.columns = inventory.columns.str.strip()
sales_lines.columns = sales_lines.columns.str.strip()
sales_header.columns = sales_header.columns.str.strip()

print("Sales Header columns:")
print(sales_header.columns.tolist())

# ---------------------------------------------------------
# Find sales date column automatically
# ---------------------------------------------------------

date_candidates = [
    "order_date",
    "sales_date",
    "so_date",
    "date",
    "created_at",
    "transaction_date",
    "order_datetime"
]

date_column = None

for column in date_candidates:
    if column in sales_header.columns:
        date_column = column
        break

if date_column is None:
    raise ValueError(
        "Sales date column was not found."
    )

# Convert date
sales_header[date_column] = pd.to_datetime(
    sales_header[date_column],
    errors="coerce"
)

# Remove invalid dates
sales_header = sales_header.dropna(
    subset=[date_column]
)

# ---------------------------------------------------------
# Identify sales order ID column
# ---------------------------------------------------------

order_id_candidates = [
    "so_id",
    "sales_order_id",
    "order_id"
]

order_id_column = None

for column in order_id_candidates:
    if column in sales_header.columns:
        order_id_column = column
        break

if order_id_column is None:
    raise ValueError(
        "Sales order ID column was not found."
    )

# ---------------------------------------------------------
# Merge sales lines with sales header
# ---------------------------------------------------------

sales_data = sales_lines.merge(
    sales_header[
        [order_id_column, date_column]
    ],
    left_on="so_id",
    right_on=order_id_column,
    how="left"
)

# Convert quantity
sales_data["quantity"] = pd.to_numeric(
    sales_data["quantity"],
    errors="coerce"
).fillna(0)

# ---------------------------------------------------------
# Last sale date for each product
# ---------------------------------------------------------

last_sale = (
    sales_data
    .groupby("product_id")
    .agg(
        last_sale_date=(date_column, "max"),
        total_quantity_sold=("quantity", "sum")
    )
    .reset_index()
)

# ---------------------------------------------------------
# Reference date
# ---------------------------------------------------------

reference_date = sales_header[date_column].max()

# Calculate days since last sale
last_sale["days_since_last_sale"] = (
    reference_date
    - last_sale["last_sale_date"]
).dt.days

last_sale["days_since_last_sale"] = (
    last_sale["days_since_last_sale"]
    .fillna(9999)
    .astype(int)
)

# ---------------------------------------------------------
# Merge with inventory
# ---------------------------------------------------------

aging = inventory.merge(
    last_sale,
    on="product_id",
    how="left"
)

aging["total_quantity_sold"] = (
    aging["total_quantity_sold"]
    .fillna(0)
)

aging["days_since_last_sale"] = (
    aging["days_since_last_sale"]
    .fillna(9999)
    .astype(int)
)

# ---------------------------------------------------------
# Convert current stock
# ---------------------------------------------------------

aging["current_stock"] = pd.to_numeric(
    aging["current_stock"],
    errors="coerce"
).fillna(0)

# ---------------------------------------------------------
# Aging category
# ---------------------------------------------------------

def aging_category(days):
    if days <= 30:
        return "0-30 Days"
    elif days <= 60:
        return "31-60 Days"
    elif days <= 90:
        return "61-90 Days"
    elif days <= 180:
        return "91-180 Days"
    else:
        return "180+ Days"

aging["aging_category"] = (
    aging["days_since_last_sale"]
    .apply(aging_category)
)

# ---------------------------------------------------------
# Aging risk
# ---------------------------------------------------------

def aging_risk(row):

    days = row["days_since_last_sale"]
    stock = row["current_stock"]

    if stock > 0 and days > 180:
        return "High Risk"

    elif stock > 0 and days > 90:
        return "Medium Risk"

    else:
        return "Low Risk"

aging["aging_risk"] = (
    aging.apply(
        aging_risk,
        axis=1
    )
)

# ---------------------------------------------------------
# Aging score
# ---------------------------------------------------------

def aging_score(days):

    if days <= 30:
        return 100
    elif days <= 60:
        return 80
    elif days <= 90:
        return 60
    elif days <= 180:
        return 40
    else:
        return 20

aging["aging_score"] = (
    aging["days_since_last_sale"]
    .apply(aging_score)
)

# ---------------------------------------------------------
# Sort oldest inventory first
# ---------------------------------------------------------

aging = aging.sort_values(
    by="days_since_last_sale",
    ascending=False
)

# ---------------------------------------------------------
# Save output
# ---------------------------------------------------------

output_file = (
    FEATURE_DIR /
    "inventory_aging.csv"
)

aging.to_csv(
    output_file,
    index=False
)

# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print(
    "\nInventory Aging Analysis completed successfully."
)

print(
    f"Output saved to: {output_file}"
)

print(
    f"Total inventory records analysed: "
    f"{len(aging)}"
)

print("\nAging Category Summary:")

print(
    aging["aging_category"]
    .value_counts()
)

print("\nAging Risk Summary:")

print(
    aging["aging_risk"]
    .value_counts()
)

print("\nOldest Inventory Records:")

print(
    aging[
        [
            "product_id",
            "current_stock",
            "last_sale_date",
            "days_since_last_sale",
            "aging_category",
            "aging_risk"
        ]
    ].head(10)
)