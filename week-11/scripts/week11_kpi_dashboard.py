from pathlib import Path
import pandas as pd
import numpy as np


# Project folders
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "week-11" / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_csv(filename):
    file_path = DATA_DIR / filename

    if file_path.exists():
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower()
        print(f"Loaded: {filename}")
        return df

    print(f"Missing file: {filename}")
    return pd.DataFrame()


def save_csv(df, filename):
    output_path = OUTPUT_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"Created: {filename}")


def find_column(df, columns):
    for column in columns:
        if column in df.columns:
            return column
    return None


# ==========================================
# 1. LOAD ALL DATASETS
# ==========================================

products = load_csv("products.csv")
inventory = load_csv("inventory_master.csv")
sales = load_csv("sales_orders_lines.csv")
suppliers = load_csv("suppliers.csv")
purchase_lines = load_csv("purchase_orders_lines.csv")
branches = load_csv("branches.csv")
customers = load_csv("customers.csv")


# ==========================================
# 2. KPI SUMMARY
# ==========================================

kpis = []


def add_kpi(kpi_name, value, unit):
    kpis.append({
        "KPI": kpi_name,
        "Value": value,
        "Unit": unit
    })


add_kpi("Total Products", len(products), "Count")
add_kpi("Total Inventory Records", len(inventory), "Count")
add_kpi("Total Sales Order Lines", len(sales), "Count")
add_kpi("Total Suppliers", len(suppliers), "Count")
add_kpi("Total Branches", len(branches), "Count")
add_kpi("Total Customers", len(customers), "Count")


sales_quantity_column = find_column(
    sales,
    [
        "quantity",
        "qty",
        "order_quantity",
        "sales_quantity"
    ]
)

sales_amount_column = find_column(
    sales,
    [
        "sales_amount",
        "amount",
        "total_amount",
        "line_total",
        "revenue",
        "net_amount"
    ]
)

inventory_stock_column = find_column(
    inventory,
    [
        "current_stock",
        "quantity",
        "qty",
        "stock_quantity",
        "available_quantity",
        "on_hand"
    ]
)


if sales_quantity_column:
    sales[sales_quantity_column] = pd.to_numeric(
        sales[sales_quantity_column],
        errors="coerce"
    ).fillna(0)

    total_units_sold = sales[sales_quantity_column].sum()

    add_kpi(
        "Total Units Sold",
        total_units_sold,
        "Units"
    )


if sales_amount_column:
    sales[sales_amount_column] = pd.to_numeric(
        sales[sales_amount_column],
        errors="coerce"
    ).fillna(0)

    total_sales_value = sales[sales_amount_column].sum()

    add_kpi(
        "Total Sales Value",
        total_sales_value,
        "Currency"
    )


if inventory_stock_column:
    inventory[inventory_stock_column] = pd.to_numeric(
        inventory[inventory_stock_column],
        errors="coerce"
    ).fillna(0)

    total_inventory_units = inventory[inventory_stock_column].sum()

    add_kpi(
        "Total Current Stock",
        total_inventory_units,
        "Units"
    )


kpi_df = pd.DataFrame(kpis)

save_csv(
    kpi_df,
    "week11_kpi_summary.csv"
)


# ==========================================
# 3. PRODUCT PERFORMANCE
# ==========================================

product_id_column = find_column(
    sales,
    [
        "product_id",
        "product_code",
        "sku",
        "item_id"
    ]
)

if product_id_column:

    aggregation = {}

    if sales_quantity_column:
        aggregation[sales_quantity_column] = "sum"

    if sales_amount_column:
        aggregation[sales_amount_column] = "sum"

    if aggregation:

        product_performance = (
            sales.groupby(product_id_column)
            .agg(aggregation)
            .reset_index()
        )

        rename_columns = {}

        if sales_quantity_column:
            rename_columns[sales_quantity_column] = "units_sold"

        if sales_amount_column:
            rename_columns[sales_amount_column] = "sales_value"

        product_performance.rename(
            columns=rename_columns,
            inplace=True
        )

        sort_column = (
            "sales_value"
            if "sales_value" in product_performance.columns
            else "units_sold"
        )

        product_performance = product_performance.sort_values(
            by=sort_column,
            ascending=False
        )

        save_csv(
            product_performance,
            "product_performance_dashboard.csv"
        )


# ==========================================
# 4. INVENTORY HEALTH
# ==========================================

if inventory_stock_column:

    inventory["stock_status"] = np.select(
        [
            inventory[inventory_stock_column] <= 0,
            inventory[inventory_stock_column] < inventory[
                inventory_stock_column
            ].median()
        ],
        [
            "Stockout",
            "Low Stock"
        ],
        default="Healthy"
    )

    reorder_column = find_column(
        inventory,
        [
            "reorder_level",
            "reorder_point",
            "minimum_stock",
            "min_stock"
        ]
    )

    if reorder_column:

        inventory[reorder_column] = pd.to_numeric(
            inventory[reorder_column],
            errors="coerce"
        ).fillna(0)

        inventory["stock_status"] = np.select(
            [
                inventory[inventory_stock_column] <= 0,
                inventory[inventory_stock_column]
                <= inventory[reorder_column]
            ],
            [
                "Stockout",
                "Reorder Required"
            ],
            default="Healthy"
        )

    save_csv(
        inventory,
        "inventory_health_dashboard.csv"
    )

    inventory_status = (
        inventory["stock_status"]
        .value_counts()
        .reset_index()
    )

    inventory_status.columns = [
        "stock_status",
        "count"
    ]

    save_csv(
        inventory_status,
        "inventory_status_summary.csv"
    )


# ==========================================
# 5. SUPPLIER PERFORMANCE
# ==========================================

supplier_id_column = find_column(
    purchase_lines,
    [
        "supplier_id",
        "supplier_code",
        "vendor_id"
    ]
)

purchase_quantity_column = find_column(
    purchase_lines,
    [
        "quantity",
        "qty",
        "order_quantity"
    ]
)

purchase_amount_column = find_column(
    purchase_lines,
    [
        "amount",
        "total_amount",
        "line_total",
        "purchase_amount",
        "cost"
    ]
)


if supplier_id_column:

    supplier_aggregation = {}

    if purchase_quantity_column:

        purchase_lines[purchase_quantity_column] = pd.to_numeric(
            purchase_lines[purchase_quantity_column],
            errors="coerce"
        ).fillna(0)

        supplier_aggregation[
            purchase_quantity_column
        ] = "sum"

    if purchase_amount_column:

        purchase_lines[purchase_amount_column] = pd.to_numeric(
            purchase_lines[purchase_amount_column],
            errors="coerce"
        ).fillna(0)

        supplier_aggregation[
            purchase_amount_column
        ] = "sum"

    if supplier_aggregation:

        supplier_performance = (
            purchase_lines.groupby(supplier_id_column)
            .agg(supplier_aggregation)
            .reset_index()
        )

        rename_columns = {}

        if purchase_quantity_column:
            rename_columns[
                purchase_quantity_column
            ] = "units_ordered"

        if purchase_amount_column:
            rename_columns[
                purchase_amount_column
            ] = "purchase_value"

        supplier_performance.rename(
            columns=rename_columns,
            inplace=True
        )

        save_csv(
            supplier_performance,
            "supplier_performance_dashboard.csv"
        )


# ==========================================
# 6. BRANCH INVENTORY
# ==========================================

branch_id_column = find_column(
    inventory,
    [
        "branch_id",
        "warehouse_id",
        "location_id",
        "store_id"
    ]
)


if branch_id_column and inventory_stock_column:

    branch_inventory = (
        inventory.groupby(branch_id_column)
        .agg(
            inventory_units=(
                inventory_stock_column,
                "sum"
            ),
            inventory_records=(
                inventory_stock_column,
                "count"
            )
        )
        .reset_index()
    )

    save_csv(
        branch_inventory,
        "branch_inventory_dashboard.csv"
    )


# ==========================================
# 7. DASHBOARD BUILD GUIDE
# ==========================================

dashboard_guide = pd.DataFrame([
    {
        "Dashboard": "Executive KPI Dashboard",
        "Source File": "week11_kpi_summary.csv",
        "Recommended Visual": "KPI Cards"
    },
    {
        "Dashboard": "Product Performance",
        "Source File": "product_performance_dashboard.csv",
        "Recommended Visual": "Top 10 Products Bar Chart"
    },
    {
        "Dashboard": "Inventory Health",
        "Source File": "inventory_status_summary.csv",
        "Recommended Visual": "Stock Status Bar Chart"
    },
    {
        "Dashboard": "Supplier Performance",
        "Source File": "supplier_performance_dashboard.csv",
        "Recommended Visual": "Supplier Ranking Chart"
    },
    {
        "Dashboard": "Branch Inventory",
        "Source File": "branch_inventory_dashboard.csv",
        "Recommended Visual": "Branch Inventory Chart"
    }
])

save_csv(
    dashboard_guide,
    "dashboard_build_guide.csv"
)


print("")
print("====================================")
print("WEEK 11 COMPLETED SUCCESSFULLY")
print("====================================")