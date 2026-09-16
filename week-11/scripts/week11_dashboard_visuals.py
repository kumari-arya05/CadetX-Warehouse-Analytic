from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = ROOT / "week-11" / "outputs"
DASHBOARD_DIR = ROOT / "week-11" / "dashboards"

DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)


def read_file(filename):
    path = OUTPUT_DIR / filename

    if path.exists():
        return pd.read_csv(path)

    print(f"File not found: {filename}")
    return pd.DataFrame()


def save_chart(filename):
    plt.tight_layout()
    plt.savefig(
        DASHBOARD_DIR / filename,
        dpi=150,
        bbox_inches="tight"
    )
    plt.close()
    print(f"Created: {filename}")


# 1. Executive KPI Dashboard
kpi = read_file("week11_kpi_summary.csv")

if not kpi.empty:
    plt.figure(figsize=(12, 6))
    plt.bar(kpi["KPI"], kpi["Value"])

    plt.title("Week 11 Executive KPI Dashboard")
    plt.xlabel("KPI")
    plt.ylabel("Value")
    plt.xticks(rotation=45, ha="right")

    save_chart("executive_kpi_dashboard.png")


# 2. Product Performance Dashboard
products = read_file("product_performance_dashboard.csv")

if not products.empty:
    value_column = None

    if "sales_value" in products.columns:
        value_column = "sales_value"
    elif "units_sold" in products.columns:
        value_column = "units_sold"

    if value_column:
        product_column = products.columns[0]

        top_products = products.sort_values(
            value_column,
            ascending=False
        ).head(10)

        plt.figure(figsize=(12, 6))
        plt.bar(
            top_products[product_column].astype(str),
            top_products[value_column]
        )

        plt.title("Top 10 Product Performance")
        plt.xlabel("Product")
        plt.ylabel(value_column)
        plt.xticks(rotation=45, ha="right")

        save_chart("product_performance_dashboard.png")


# 3. Inventory Health Dashboard
inventory = read_file("inventory_status_summary.csv")

if not inventory.empty:
    plt.figure(figsize=(8, 6))
    plt.bar(
        inventory["stock_status"],
        inventory["count"]
    )

    plt.title("Inventory Health Status")
    plt.xlabel("Stock Status")
    plt.ylabel("Number of Records")
    plt.xticks(rotation=20)

    save_chart("inventory_health_dashboard.png")


# 4. Supplier Performance Dashboard
suppliers = read_file("supplier_performance_dashboard.csv")

if not suppliers.empty:
    value_column = None

    if "purchase_value" in suppliers.columns:
        value_column = "purchase_value"
    elif "units_ordered" in suppliers.columns:
        value_column = "units_ordered"

    if value_column:
        supplier_column = suppliers.columns[0]

        top_suppliers = suppliers.sort_values(
            value_column,
            ascending=False
        ).head(10)

        plt.figure(figsize=(12, 6))
        plt.bar(
            top_suppliers[supplier_column].astype(str),
            top_suppliers[value_column]
        )

        plt.title("Top 10 Supplier Performance")
        plt.xlabel("Supplier")
        plt.ylabel(value_column)
        plt.xticks(rotation=45, ha="right")

        save_chart("supplier_performance_dashboard.png")


# 5. Branch Inventory Dashboard
branches = read_file("branch_inventory_dashboard.csv")

if not branches.empty:
    if "inventory_units" in branches.columns:
        branch_column = branches.columns[0]

        plt.figure(figsize=(12, 6))
        plt.bar(
            branches[branch_column].astype(str),
            branches["inventory_units"]
        )

        plt.title("Inventory by Branch/Warehouse")
        plt.xlabel("Branch/Warehouse")
        plt.ylabel("Inventory Units")
        plt.xticks(rotation=45, ha="right")

        save_chart("branch_inventory_dashboard.png")


print("Week 11 dashboard visuals completed successfully.")