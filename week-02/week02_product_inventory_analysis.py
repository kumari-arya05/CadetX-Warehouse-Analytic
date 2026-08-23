import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# WEEK 02 - PRODUCT & INVENTORY ANALYTICS
# ==========================================

# ==========================================
# 1. LOAD DATASETS
# ==========================================

products = pd.read_csv("data/products.csv")
inventory = pd.read_csv("data/inventory_master.csv")
sales = pd.read_csv("data/sales_orders_lines.csv")
sales_header = pd.read_csv("data/sales_orders_header.csv")

# ==========================================
# 2. PRODUCT SALES DATA
# ==========================================

product_sales = (
    sales.groupby("product_id")
    .agg(
        total_quantity_sold=("quantity", "sum"),
        total_sales_value=("line_grand_total", "sum")
    )
    .reset_index()
)

# ==========================================
# 3. PRODUCT PERFORMANCE
# ==========================================

product_performance = product_sales.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "brand",
            "unit_cost",
            "unit_price",
            "margin_percentage"
        ]
    ],
    on="product_id",
    how="left"
)

product_performance = product_performance.sort_values(
    "total_sales_value",
    ascending=False
)

product_performance.to_csv(
    "week-02/product_performance_analysis.csv",
    index=False
)

print("Product performance analysis saved successfully.")

# ==========================================
# 4. FAST-MOVING PRODUCTS
# ==========================================

fast_moving_products = product_sales.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "brand",
            "usage_frequency"
        ]
    ],
    on="product_id",
    how="left"
)

fast_moving_products = fast_moving_products.sort_values(
    "total_quantity_sold",
    ascending=False
)

fast_moving_products.to_csv(
    "week-02/fast_moving_products.csv",
    index=False
)

print("Fast-moving product analysis saved successfully.")

# ==========================================
# 5. SLOW-MOVING & DEAD STOCK
# ==========================================

slow_dead_stock = product_sales.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "brand",
            "usage_frequency"
        ]
    ],
    on="product_id",
    how="left"
)

slow_dead_stock = slow_dead_stock.merge(
    inventory[
        [
            "product_id",
            "current_stock",
            "reorder_level",
            "safety_stock",
            "max_stock"
        ]
    ],
    on="product_id",
    how="left"
)

slow_dead_stock["stock_to_sales_ratio"] = (
    slow_dead_stock["current_stock"]
    / slow_dead_stock["total_quantity_sold"].replace(0, np.nan)
)

slow_dead_stock = slow_dead_stock.sort_values(
    "total_quantity_sold",
    ascending=True
)

slow_dead_stock.to_csv(
    "week-02/slow_moving_dead_stock.csv",
    index=False
)

print("Slow-moving and dead-stock analysis saved successfully.")

# ==========================================
# 6. INVENTORY TURNOVER
# ==========================================

inventory_turnover = product_sales.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "unit_cost"
        ]
    ],
    on="product_id",
    how="left"
)

inventory_turnover = inventory_turnover.merge(
    inventory[
        [
            "product_id",
            "current_stock"
        ]
    ],
    on="product_id",
    how="left"
)

inventory_turnover["cost_of_goods_sold"] = (
    inventory_turnover["total_quantity_sold"]
    * inventory_turnover["unit_cost"]
)

inventory_turnover["inventory_turnover_ratio"] = (
    inventory_turnover["total_quantity_sold"]
    / inventory_turnover["current_stock"].replace(0, np.nan)
)

inventory_turnover = inventory_turnover.sort_values(
    "inventory_turnover_ratio",
    ascending=False
)

inventory_turnover.to_csv(
    "week-02/inventory_turnover_analysis.csv",
    index=False
)

print("Inventory turnover analysis saved successfully.")

# ==========================================
# 7. STOCK HEALTH ASSESSMENT
# ==========================================

stock_health = inventory.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "brand",
            "criticality_level"
        ]
    ],
    on="product_id",
    how="left"
)

stock_health["stock_above_reorder"] = (
    stock_health["current_stock"]
    - stock_health["reorder_level"]
)

stock_health["stock_above_safety"] = (
    stock_health["current_stock"]
    - stock_health["safety_stock"]
)

def classify_stock(row):
    if row["current_stock"] <= row["safety_stock"]:
        return "Critical"
    elif row["current_stock"] <= row["reorder_level"]:
        return "Low Stock"
    elif row["current_stock"] >= row["max_stock"]:
        return "Overstock"
    else:
        return "Healthy"

stock_health["stock_health_status"] = stock_health.apply(
    classify_stock,
    axis=1
)

stock_health.to_csv(
    "week-02/stock_health_assessment.csv",
    index=False
)

print("Stock health assessment saved successfully.")

# ==========================================
# 8. INVENTORY AGING ANALYSIS
# ==========================================

inventory_aging = inventory.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "brand",
            "last_purchase_date"
        ]
    ],
    on="product_id",
    how="left"
)

inventory_aging["last_purchase_date"] = pd.to_datetime(
    inventory_aging["last_purchase_date"],
    errors="coerce"
)

reference_date = inventory_aging["last_purchase_date"].max()

inventory_aging["estimated_age_days"] = (
    reference_date - inventory_aging["last_purchase_date"]
).dt.days

def classify_age(days):
    if pd.isna(days):
        return "Unknown"
    elif days <= 90:
        return "0-90 Days"
    elif days <= 180:
        return "91-180 Days"
    elif days <= 365:
        return "181-365 Days"
    else:
        return "365+ Days"

inventory_aging["inventory_age_category"] = (
    inventory_aging["estimated_age_days"]
    .apply(classify_age)
)

inventory_aging.to_csv(
    "week-02/inventory_aging_analysis.csv",
    index=False
)

print("Inventory aging analysis saved successfully.")

# ==========================================
# 9. ABC / PARETO PRODUCT CLASSIFICATION
# ==========================================

abc_analysis = product_sales[
    [
        "product_id",
        "total_quantity_sold",
        "total_sales_value"
    ]
].copy()

abc_analysis = abc_analysis.sort_values(
    "total_sales_value",
    ascending=False
).reset_index(drop=True)

total_sales = abc_analysis["total_sales_value"].sum()

abc_analysis["sales_contribution_percentage"] = (
    abc_analysis["total_sales_value"]
    / total_sales
) * 100

abc_analysis["cumulative_sales_percentage"] = (
    abc_analysis["sales_contribution_percentage"].cumsum()
)

def classify_abc(cumulative_percentage):
    if cumulative_percentage <= 80:
        return "A"
    elif cumulative_percentage <= 95:
        return "B"
    else:
        return "C"

abc_analysis["abc_class"] = (
    abc_analysis["cumulative_sales_percentage"]
    .apply(classify_abc)
)

abc_analysis = abc_analysis.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "brand"
        ]
    ],
    on="product_id",
    how="left"
)

abc_analysis.to_csv(
    "week-02/abc_pareto_product_classification.csv",
    index=False
)

print("ABC / Pareto product classification saved successfully.")

# ==========================================
# 10. OVERSTOCK & UNDERSTOCK DETECTION
# ==========================================

stock_analysis = inventory.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "brand",
            "criticality_level"
        ]
    ],
    on="product_id",
    how="left"
)

stock_analysis["stock_vs_reorder"] = (
    stock_analysis["current_stock"]
    - stock_analysis["reorder_level"]
)

stock_analysis["stock_vs_max"] = (
    stock_analysis["current_stock"]
    - stock_analysis["max_stock"]
)

def classify_inventory(row):
    if row["current_stock"] < row["reorder_level"]:
        return "Understock"
    elif row["current_stock"] > row["max_stock"]:
        return "Overstock"
    else:
        return "Optimal"

stock_analysis["inventory_status"] = stock_analysis.apply(
    classify_inventory,
    axis=1
)

stock_analysis.to_csv(
    "week-02/overstock_understock_detection.csv",
    index=False
)

print("Overstock and understock analysis saved successfully.")

# ==========================================
# 11. PRODUCT DEMAND TREND ANALYSIS
# ==========================================

# Convert order date to datetime
sales_header["order_date"] = pd.to_datetime(
    sales_header["order_date"],
    errors="coerce"
)

# Connect sales lines with order dates
sales_with_dates = sales.merge(
    sales_header[
        [
            "so_id",
            "order_date"
        ]
    ],
    on="so_id",
    how="left"
)

# Create monthly demand
sales_with_dates["order_month"] = (
    sales_with_dates["order_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_product_demand = (
    sales_with_dates.groupby(
        ["product_id", "order_month"]
    )
    .agg(
        total_quantity_sold=("quantity", "sum"),
        total_sales_value=("line_grand_total", "sum")
    )
    .reset_index()
)

# Add product details
monthly_product_demand = monthly_product_demand.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "brand"
        ]
    ],
    on="product_id",
    how="left"
)

# Sort by product and month
monthly_product_demand = monthly_product_demand.sort_values(
    ["product_id", "order_month"]
)

print("\n===== PRODUCT DEMAND TREND ANALYSIS =====")
print(monthly_product_demand.head(20))

# Save monthly demand trend
monthly_product_demand.to_csv(
    "week-02/product_demand_trend_analysis.csv",
    index=False
)

print("Product demand trend analysis saved successfully.")

# ==========================================
# 12. TOP PRODUCTS BY TOTAL DEMAND
# ==========================================

top_demand_products = (
    monthly_product_demand.groupby(
        ["product_id", "product_name", "category", "brand"]
    )
    .agg(
        total_demand=("total_quantity_sold", "sum")
    )
    .reset_index()
    .sort_values(
        "total_demand",
        ascending=False
    )
)

top_demand_products.to_csv(
    "week-02/top_demand_products.csv",
    index=False
)

print("Top demand products saved successfully.")

# ==========================================
# 13. WEEK 02 FINAL STATUS
# ==========================================

print(
    "\n===== WEEK 02 TASK 1, TASK 2, TASK 3, "
    "TASK 4, TASK 5, TASK 6, TASK 7, TASK 8 "
    "& TASK 9 COMPLETE ====="
)