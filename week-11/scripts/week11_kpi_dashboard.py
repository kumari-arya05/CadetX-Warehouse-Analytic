from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "week-11" / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_file(filename):
    file_path = DATA_DIR / filename

    if file_path.exists():
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower()
        print(f"Loaded: {filename}")
        return df

    print(f"Missing file: {filename}")
    return pd.DataFrame()


def find_column(df, possible_columns):
    for column in possible_columns:
        if column in df.columns:
            return column
    return None


def save_file(df, filename):
    output_path = OUTPUT_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"Created: {filename}")


# Load datasets
products = load_file("products.csv")
inventory = load_file("inventory_master.csv")
sales = load_file("sales_orders_lines.csv")
suppliers = load_file("suppliers.csv")
branches = load_file("branches.csv")
customers = load_file("customers.csv")
purchase_lines = load_file("purchase_orders_lines.csv")


# -------------------------------
# 1. KPI SUMMARY
# -------------------------------

kpis = []

kpis.append(["Products", len(products)])
kpis.append(["Inventory Records", len(inventory)])
kpis.append(["Sales Order Lines", len(sales)])
kpis.append(["Suppliers", len(suppliers)])
kpis.append(["Branches", len(branches)])
kpis.append(["Customers", len(customers)])

sales_quantity = find_column(
    sales,
    ["quantity", "qty", "order_quantity", "sales_quantity"]
)

sales_amount = find_column(
    sales,
    ["sales_amount", "amount", "total_amount", "line_total", "revenue"]
)

inventory_quantity = find_column(
    inventory,
    ["quantity", "qty", "stock_quantity", "available_quantity", "on_hand"]
)

if sales_quantity:
    total_units = pd.to_numeric(
        sales[sales_quantity], errors="coerce"
    ).fillna(0).sum()

    kpis.append(["Total Units Sold", total_units])

if sales_amount:
    total_sales = pd.to_numeric(
        sales[sales_amount], errors="coerce"
    ).fillna(0).sum()

    kpis.append(["Total Sales Value", total_sales])

if inventory_quantity:
    total_inventory = pd.to_numeric(
        inventory[inventory_quantity], errors="coerce"
    ).fillna(0).sum()

    kpis.append(["Total Inventory Units", total_inventory])

kpi_df = pd.DataFrame(kpis, columns=["KPI", "Value"])
save_file(kpi_df, "week11_kpi_summary.csv")


# -------------------------------
# 2. PRODUCT PERFORMANCE
# -------------------------------

product_column = find_column(
    sales,
    ["product_id", "product_code", "sku", "item_id"]
)

if product_column:
    sales_copy = sales.copy()

    if sales_quantity:
        sales_copy[sales_quantity] = pd.to_numeric(
            sales_copy[sales_quantity], errors="coerce"
        ).fillna(0)

    if sales_amount:
        sales_copy[sales_amount] = pd.to_numeric(
            sales_copy[sales_amount], errors="coerce"
        ).fillna(0)

    aggregation = {}

    if sales_quantity:
        aggregation[sales_quantity] = "sum"

    if sales_amount:
        aggregation[sales_amount] = "sum"

    if aggregation:
        product_performance = (
            sales_copy.groupby(product_column)
            .agg(aggregation)
            .reset_index()
        )

        product_performance.rename(
            columns={
                sales_quantity: "units_sold"
                if sales_quantity else sales_quantity,
                sales_amount: "sales_value"
                if sales_amount else sales_amount
            },
            inplace=True
        )

        save_file(
            product_performance,
            "product_performance_dashboard.csv"
        )


# -------------------------------
# 3. INVENTORY HEALTH
# -------------------------------

if inventory_quantity:
    inventory_copy = inventory.copy()

    inventory_copy[inventory_quantity] = pd.to_numeric(
        inventory_copy[inventory_quantity], errors="coerce"
    ).fillna(0)

    median_stock = inventory_copy[inventory_quantity].median()

    inventory_copy["stock_status"] = np.select(
        [
            inventory_copy[inventory_quantity] <= 0,
            inventory_copy[inventory_quantity] < median_stock
        ],
        [
            "Stockout",
            "Low Stock"
        ],
        default="Healthy"
    )

    save_file(
        inventory_copy,
        "inventory_health_dashboard.csv"
    )

    inventory_status = (
        inventory_copy["stock_status"]
        .value_counts()
        .reset_index()
    )

    inventory_status.columns = ["stock_status", "count"]

    save_file(
        inventory_status,
        "inventory_status_summary.csv"
    )


# -------------------------------
# 4. SUPPLIER PERFORMANCE
# -------------------------------

supplier_column = find_column(
    purchase_lines,
    ["supplier_id", "supplier_code", "vendor_id"]
)

purchase_quantity = find_column(
    purchase_lines,
    ["quantity", "qty", "order_quantity"]
)

purchase_amount = find_column(
    purchase_lines,
    ["amount", "total_amount", "line_total", "purchase_amount", "cost"]
)

if supplier_column:
    supplier_copy = purchase_lines.copy()
    aggregation = {}

    if purchase_quantity:
        supplier_copy[purchase_quantity] = pd.to_numeric(
            supplier_copy[purchase_quantity], errors="coerce"
        ).fillna(0)

        aggregation[purchase_quantity] = "sum"

    if purchase_amount:
        supplier_copy[purchase_amount] = pd.to_numeric(
            supplier_copy[purchase_amount], errors="coerce"
        ).fillna(0)

        aggregation[purchase_amount] = "sum"

    if aggregation:
        supplier_performance = (
            supplier_copy.groupby(supplier_column)
            .agg(aggregation)
            .reset_index()
        )

        save_file(
            supplier_performance,
            "supplier_performance_dashboard.csv"
        )


# -------------------------------
# 5. BRANCH INVENTORY
# -------------------------------

branch_column = find_column(
    inventory,
    ["branch_id", "warehouse_id", "location_id", "store_id"]
)

if branch_column and inventory_quantity:
    branch_copy = inventory.copy()

    branch_copy[inventory_quantity] = pd.to_numeric(
        branch_copy[inventory_quantity], errors="coerce"
    ).fillna(0)

    branch_summary = (
        branch_copy.groupby(branch_column)
        .agg(
            inventory_units=(inventory_quantity, "sum"),
            inventory_records=(inventory_quantity, "count")
        )
        .reset_index()
    )

    save_file(
        branch_summary,
        "branch_inventory_dashboard.csv"
    )


# -------------------------------
# 6. DASHBOARD GUIDE
# -------------------------------

dashboard_guide = pd.DataFrame([
    [
        "Executive KPI Dashboard",
        "week11_kpi_summary.csv",
        "KPI Cards"
    ],
    [
        "Product Performance",
        "product_performance_dashboard.csv",
        "Bar Chart"
    ],
    [
        "Inventory Health",
        "inventory_status_summary.csv",
        "Donut Chart / Bar Chart"
    ],
    [
        "Supplier Performance",
        "supplier_performance_dashboard.csv",
        "Supplier Ranking"
    ],
    [
        "Branch Inventory",
        "branch_inventory_dashboard.csv",
        "Branch Comparison"
    ]
], columns=["Dashboard", "Source File", "Recommended Visual"])

save_file(
    dashboard_guide,
    "dashboard_build_guide.csv"
)

print("Week 11 analytics completed successfully.")