import pandas as pd
from pathlib import Path


# ============================================================
# WEEK 03 - DATA INTEGRATION & DATASET MERGING
# ============================================================

print("=" * 70)
print("WEEK 03 - DATA INTEGRATION & DATASET MERGING")
print("=" * 70)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
CLEANED_DIR = DATA_DIR / "cleaned"
INTEGRATED_DIR = DATA_DIR / "integrated"

INTEGRATED_DIR.mkdir(parents=True, exist_ok=True)

print(f"Project root: {PROJECT_ROOT}")
print(f"Cleaned data folder: {CLEANED_DIR}")
print(f"Integrated data folder: {INTEGRATED_DIR}")


# ============================================================
# 2. LOAD CLEANED DATASETS
# ============================================================

products_file = CLEANED_DIR / "products_cleaned.csv"
inventory_file = CLEANED_DIR / "inventory_cleaned.csv"
sales_lines_file = CLEANED_DIR / "sales_orders_lines_cleaned.csv"
sales_header_file = CLEANED_DIR / "sales_orders_header_cleaned.csv"

required_files = [
    products_file,
    inventory_file,
    sales_lines_file,
    sales_header_file
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file not found: {file_path}"
        )

products = pd.read_csv(products_file)
inventory = pd.read_csv(inventory_file)
sales_lines = pd.read_csv(sales_lines_file)
sales_header = pd.read_csv(sales_header_file)


print()
print("Datasets loaded successfully.")

print(f"Products: {products.shape}")
print(f"Inventory: {inventory.shape}")
print(f"Sales order lines: {sales_lines.shape}")
print(f"Sales order header: {sales_header.shape}")


# ============================================================
# 3. STANDARDIZE COLUMN NAMES
# ============================================================

def standardize_columns(df):
    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return df


products = standardize_columns(products)
inventory = standardize_columns(inventory)
sales_lines = standardize_columns(sales_lines)
sales_header = standardize_columns(sales_header)


# ============================================================
# 4. PRODUCT + INVENTORY INTEGRATION
# ============================================================

if "product_id" not in products.columns:
    raise KeyError("product_id not found in products dataset.")

if "product_id" not in inventory.columns:
    raise KeyError("product_id not found in inventory dataset.")

if "product_id" not in sales_lines.columns:
    raise KeyError(
        "product_id not found in sales order lines dataset."
    )


products["product_id"] = products["product_id"].astype("string")
inventory["product_id"] = inventory["product_id"].astype("string")
sales_lines["product_id"] = sales_lines["product_id"].astype("string")


product_inventory = products.merge(
    inventory,
    on="product_id",
    how="left",
    suffixes=("_product", "_inventory")
)


product_inventory_file = (
    INTEGRATED_DIR / "product_inventory_integrated.csv"
)

product_inventory.to_csv(
    product_inventory_file,
    index=False
)

print()
print("-" * 70)
print("PRODUCT + INVENTORY INTEGRATION COMPLETE")
print("-" * 70)
print(f"Rows: {len(product_inventory)}")
print(f"Columns: {len(product_inventory.columns)}")
print(f"Saved: {product_inventory_file}")


# ============================================================
# 5. SALES + PRODUCT INTEGRATION
# ============================================================

sales_product = sales_lines.merge(
    products,
    on="product_id",
    how="left",
    suffixes=("_sales", "_product")
)


sales_product_file = (
    INTEGRATED_DIR / "sales_product_integrated.csv"
)

sales_product.to_csv(
    sales_product_file,
    index=False
)

print()
print("-" * 70)
print("SALES + PRODUCT INTEGRATION COMPLETE")
print("-" * 70)
print(f"Rows: {len(sales_product)}")
print(f"Columns: {len(sales_product.columns)}")
print(f"Saved: {sales_product_file}")


# ============================================================
# 6. SALES LINES + SALES HEADER
# ============================================================

# CadetX sales order datasets use so_id
ORDER_KEY = "so_id"


if ORDER_KEY not in sales_lines.columns:
    raise KeyError(
        f"{ORDER_KEY} not found in sales order lines dataset."
    )

if ORDER_KEY not in sales_header.columns:
    raise KeyError(
        f"{ORDER_KEY} not found in sales order header dataset."
    )


sales_lines[ORDER_KEY] = (
    sales_lines[ORDER_KEY].astype("string")
)

sales_header[ORDER_KEY] = (
    sales_header[ORDER_KEY].astype("string")
)


sales_order = sales_lines.merge(
    sales_header,
    on=ORDER_KEY,
    how="left",
    suffixes=("_line", "_header")
)


sales_order_file = (
    INTEGRATED_DIR / "sales_orders_integrated.csv"
)

sales_order.to_csv(
    sales_order_file,
    index=False
)


print()
print("-" * 70)
print("SALES LINES + SALES HEADER INTEGRATION COMPLETE")
print("-" * 70)
print(f"Merge key: {ORDER_KEY}")
print(f"Rows: {len(sales_order)}")
print(f"Columns: {len(sales_order.columns)}")
print(f"Saved: {sales_order_file}")


# ============================================================
# 7. PRODUCT SALES SUMMARY
# ============================================================

if "quantity" not in sales_lines.columns:
    raise KeyError(
        "quantity column not found in sales order lines."
    )


if "line_grand_total" in sales_lines.columns:

    product_sales = (
        sales_lines
        .groupby("product_id")
        .agg(
            total_quantity_sold=("quantity", "sum"),
            total_sales_value=("line_grand_total", "sum")
        )
        .reset_index()
    )

else:

    product_sales = (
        sales_lines
        .groupby("product_id")
        .agg(
            total_quantity_sold=("quantity", "sum")
        )
        .reset_index()
    )

    product_sales["total_sales_value"] = 0


# ============================================================
# 8. PRODUCT + INVENTORY + SALES MASTER
# ============================================================

product_inventory_sales = product_inventory.merge(
    product_sales,
    on="product_id",
    how="left"
)


product_inventory_sales["total_quantity_sold"] = (
    product_inventory_sales["total_quantity_sold"]
    .fillna(0)
)

product_inventory_sales["total_sales_value"] = (
    product_inventory_sales["total_sales_value"]
    .fillna(0)
)


master_product_file = (
    INTEGRATED_DIR /
    "product_inventory_sales_master.csv"
)

product_inventory_sales.to_csv(
    master_product_file,
    index=False
)


print()
print("-" * 70)
print("PRODUCT + INVENTORY + SALES MASTER COMPLETE")
print("-" * 70)
print(f"Rows: {len(product_inventory_sales)}")
print(f"Columns: {len(product_inventory_sales.columns)}")
print(f"Saved: {master_product_file}")


# ============================================================
# 9. INTEGRATION QUALITY CHECKS
# ============================================================

print()
print("=" * 70)
print("INTEGRATION QUALITY CHECKS")
print("=" * 70)


sales_product_unmatched = (
    ~sales_lines["product_id"]
    .isin(products["product_id"])
).sum()


inventory_product_unmatched = (
    ~inventory["product_id"]
    .isin(products["product_id"])
).sum()


sales_order_unmatched = (
    ~sales_lines[ORDER_KEY]
    .isin(sales_header[ORDER_KEY])
).sum()


print(
    f"Sales products without product match: "
    f"{sales_product_unmatched}"
)

print(
    f"Inventory products without product match: "
    f"{inventory_product_unmatched}"
)

print(
    f"Sales orders without header match: "
    f"{sales_order_unmatched}"
)


# ============================================================
# 10. INTEGRATION SUMMARY
# ============================================================

integration_summary = pd.DataFrame(
    {
        "integration_check": [
            "sales_product_unmatched",
            "inventory_product_unmatched",
            "sales_order_unmatched"
        ],
        "unmatched_records": [
            sales_product_unmatched,
            inventory_product_unmatched,
            sales_order_unmatched
        ]
    }
)


summary_file = (
    INTEGRATED_DIR /
    "week03_integration_summary.csv"
)

integration_summary.to_csv(
    summary_file,
    index=False
)


# ============================================================
# 11. FINAL STATUS
# ============================================================

print()
print("=" * 70)
print("WEEK 03 - DATA INTEGRATION COMPLETE")
print("=" * 70)

print(f"Integrated output folder: {INTEGRATED_DIR}")
print(f"Integration summary: {summary_file}")
print()
print("All integration outputs generated successfully.")