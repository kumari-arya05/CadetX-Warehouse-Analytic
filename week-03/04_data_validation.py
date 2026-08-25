import pandas as pd
from pathlib import Path


# ============================================================
# WEEK 03 - DATA VALIDATION & CONSISTENCY CHECKS
# ============================================================

print("=" * 70)
print("WEEK 03 - DATA VALIDATION & CONSISTENCY CHECKS")
print("=" * 70)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
CLEANED_DIR = DATA_DIR / "cleaned"
INTEGRATED_DIR = DATA_DIR / "integrated"
FEATURE_DIR = DATA_DIR / "features"
VALIDATION_DIR = DATA_DIR / "validation"

VALIDATION_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"Project root: {PROJECT_ROOT}")
print(f"Validation output folder: {VALIDATION_DIR}")


# ============================================================
# 2. FILE PATHS
# ============================================================

products_file = CLEANED_DIR / "products_cleaned.csv"
inventory_file = CLEANED_DIR / "inventory_cleaned.csv"
sales_lines_file = CLEANED_DIR / "sales_orders_lines_cleaned.csv"
sales_header_file = CLEANED_DIR / "sales_orders_header_cleaned.csv"

master_file = (
    INTEGRATED_DIR /
    "product_inventory_sales_master.csv"
)

feature_file = (
    FEATURE_DIR /
    "product_inventory_sales_features.csv"
)


required_files = [
    products_file,
    inventory_file,
    sales_lines_file,
    sales_header_file,
    master_file,
    feature_file
]


# ============================================================
# 3. CHECK REQUIRED FILES
# ============================================================

file_checks = []

for file_path in required_files:

    exists = file_path.exists()

    file_checks.append(
        {
            "file": file_path.name,
            "exists": exists
        }
    )

    status = "OK" if exists else "MISSING"

    print(
        f"{status}: {file_path.name}"
    )


missing_files = [
    item["file"]
    for item in file_checks
    if not item["exists"]
]


if missing_files:

    raise FileNotFoundError(
        "Missing required files: "
        + ", ".join(missing_files)
    )


# ============================================================
# 4. LOAD DATASETS
# ============================================================

products = pd.read_csv(products_file)
inventory = pd.read_csv(inventory_file)
sales_lines = pd.read_csv(sales_lines_file)
sales_header = pd.read_csv(sales_header_file)
master = pd.read_csv(master_file)
features = pd.read_csv(feature_file)


print()
print("All validation datasets loaded successfully.")

print(f"Products: {products.shape}")
print(f"Inventory: {inventory.shape}")
print(f"Sales lines: {sales_lines.shape}")
print(f"Sales header: {sales_header.shape}")
print(f"Master dataset: {master.shape}")
print(f"Feature dataset: {features.shape}")


# ============================================================
# 5. STANDARDIZE COLUMN NAMES
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
master = standardize_columns(master)
features = standardize_columns(features)


# ============================================================
# 6. VALIDATION RESULT STORAGE
# ============================================================

validation_results = []


def add_check(
    check_name,
    category,
    total_records,
    failed_records,
    status
):

    validation_results.append(
        {
            "check_name": check_name,
            "category": category,
            "total_records": total_records,
            "failed_records": failed_records,
            "status": status
        }
    )


# ============================================================
# 7. DUPLICATE CHECKS
# ============================================================

datasets = {
    "products": products,
    "inventory": inventory,
    "sales_lines": sales_lines,
    "sales_header": sales_header,
    "master": master,
    "features": features
}


for name, df in datasets.items():

    duplicate_rows = int(
        df.duplicated().sum()
    )

    add_check(
        check_name=f"{name}_duplicate_rows",
        category="Duplicates",
        total_records=len(df),
        failed_records=duplicate_rows,
        status="PASS"
        if duplicate_rows == 0
        else "CHECK"
    )


# ============================================================
# 8. MISSING VALUE CHECKS
# ============================================================

for name, df in datasets.items():

    missing_cells = int(
        df.isna().sum().sum()
    )

    add_check(
        check_name=f"{name}_missing_values",
        category="Missing Values",
        total_records=df.size,
        failed_records=missing_cells,
        status="PASS"
        if missing_cells == 0
        else "CHECK"
    )


# ============================================================
# 9. PRODUCT ID VALIDATION
# ============================================================

if "product_id" in products.columns:

    duplicate_product_ids = int(
        products["product_id"].duplicated().sum()
    )

    add_check(
        check_name="product_id_uniqueness",
        category="Key Integrity",
        total_records=len(products),
        failed_records=duplicate_product_ids,
        status="PASS"
        if duplicate_product_ids == 0
        else "CHECK"
    )


# ============================================================
# 10. INVENTORY PRODUCT REFERENCES
# ============================================================

if (
    "product_id" in inventory.columns
    and "product_id" in products.columns
):

    inventory_product_mismatch = int(
        (
            ~inventory["product_id"]
            .isin(products["product_id"])
        ).sum()
    )

    add_check(
        check_name="inventory_product_reference",
        category="Referential Integrity",
        total_records=len(inventory),
        failed_records=inventory_product_mismatch,
        status="PASS"
        if inventory_product_mismatch == 0
        else "CHECK"
    )


# ============================================================
# 11. SALES PRODUCT REFERENCES
# ============================================================

if (
    "product_id" in sales_lines.columns
    and "product_id" in products.columns
):

    sales_product_mismatch = int(
        (
            ~sales_lines["product_id"]
            .isin(products["product_id"])
        ).sum()
    )

    add_check(
        check_name="sales_product_reference",
        category="Referential Integrity",
        total_records=len(sales_lines),
        failed_records=sales_product_mismatch,
        status="PASS"
        if sales_product_mismatch == 0
        else "CHECK"
    )


# ============================================================
# 12. SALES ORDER REFERENCES
# ============================================================

ORDER_KEY = "so_id"


if (
    ORDER_KEY in sales_lines.columns
    and ORDER_KEY in sales_header.columns
):

    sales_order_mismatch = int(
        (
            ~sales_lines[ORDER_KEY]
            .isin(sales_header[ORDER_KEY])
        ).sum()
    )

    add_check(
        check_name="sales_order_reference",
        category="Referential Integrity",
        total_records=len(sales_lines),
        failed_records=sales_order_mismatch,
        status="PASS"
        if sales_order_mismatch == 0
        else "CHECK"
    )


# ============================================================
# 13. NUMERIC VALUE VALIDATION
# ============================================================

numeric_columns = [
    "current_stock",
    "safety_stock",
    "reorder_level",
    "max_stock",
    "unit_cost",
    "unit_price",
    "quantity",
    "total_quantity_sold",
    "total_sales_value"
]


for column in numeric_columns:

    for name, df in datasets.items():

        if column not in df.columns:
            continue

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        invalid_count = int(
            (values < 0).sum()
        )

        add_check(
            check_name=f"{name}_{column}_non_negative",
            category="Numeric Validation",
            total_records=len(df),
            failed_records=invalid_count,
            status="PASS"
            if invalid_count == 0
            else "CHECK"
        )


# ============================================================
# 14. STOCK LEVEL CONSISTENCY
# ============================================================

if all(
    column in inventory.columns
    for column in [
        "current_stock",
        "safety_stock",
        "reorder_level",
        "max_stock"
    ]
):

    stock_invalid = int(
        (
            (inventory["safety_stock"]
             > inventory["reorder_level"])
            |
            (inventory["reorder_level"]
             > inventory["max_stock"])
        ).sum()
    )

    add_check(
        check_name="inventory_level_consistency",
        category="Business Rules",
        total_records=len(inventory),
        failed_records=stock_invalid,
        status="PASS"
        if stock_invalid == 0
        else "CHECK"
    )


# ============================================================
# 15. PRICE CONSISTENCY
# ============================================================

if all(
    column in products.columns
    for column in [
        "unit_cost",
        "unit_price"
    ]
):

    price_invalid = int(
        (
            products["unit_price"]
            < products["unit_cost"]
        ).sum()
    )

    add_check(
        check_name="selling_price_vs_cost",
        category="Business Rules",
        total_records=len(products),
        failed_records=price_invalid,
        status="PASS"
        if price_invalid == 0
        else "CHECK"
    )


# ============================================================
# 16. DATE VALIDATION
# ============================================================

for name, df in datasets.items():

    for column in df.columns:

        if "date" not in column:
            continue

        parsed_dates = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        invalid_dates = int(
            (
                df[column].notna()
                &
                parsed_dates.isna()
            ).sum()
        )

        add_check(
            check_name=f"{name}_{column}_date_format",
            category="Date Validation",
            total_records=len(df),
            failed_records=invalid_dates,
            status="PASS"
            if invalid_dates == 0
            else "CHECK"
        )


# ============================================================
# 17. FEATURE DATA VALIDATION
# ============================================================

engineered_columns = [
    "stock_to_sales_ratio",
    "average_selling_price",
    "stock_above_reorder",
    "stock_to_max_ratio",
    "stock_above_safety",
    "unit_margin",
    "margin_percentage",
    "inventory_cost_value",
    "inventory_retail_value",
    "missing_value_count",
    "data_completeness_percentage"
]


for column in engineered_columns:

    if column not in features.columns:
        continue

    invalid_count = int(
        features[column].isna().sum()
    )

    add_check(
        check_name=f"feature_{column}_missing",
        category="Feature Validation",
        total_records=len(features),
        failed_records=invalid_count,
        status="PASS"
        if invalid_count == 0
        else "CHECK"
    )


# ============================================================
# 18. DATASET ROW COUNT VALIDATION
# ============================================================

add_check(
    check_name="products_not_empty",
    category="Dataset Integrity",
    total_records=1,
    failed_records=0 if len(products) > 0 else 1,
    status="PASS" if len(products) > 0 else "FAIL"
)


add_check(
    check_name="inventory_not_empty",
    category="Dataset Integrity",
    total_records=1,
    failed_records=0 if len(inventory) > 0 else 1,
    status="PASS" if len(inventory) > 0 else "FAIL"
)


add_check(
    check_name="sales_lines_not_empty",
    category="Dataset Integrity",
    total_records=1,
    failed_records=0 if len(sales_lines) > 0 else 1,
    status="PASS" if len(sales_lines) > 0 else "FAIL"
)


# ============================================================
# 19. SAVE VALIDATION REPORT
# ============================================================

validation_report = pd.DataFrame(
    validation_results
)


validation_report_file = (
    VALIDATION_DIR /
    "week03_data_validation_report.csv"
)


validation_report.to_csv(
    validation_report_file,
    index=False
)


# ============================================================
# 20. VALIDATION SUMMARY
# ============================================================

total_checks = len(validation_report)

passed_checks = int(
    (
        validation_report["status"]
        == "PASS"
    ).sum()
)

check_items = int(
    (
        validation_report["status"]
        == "CHECK"
    ).sum()
)

failed_checks = int(
    (
        validation_report["status"]
        == "FAIL"
    ).sum()
)


summary = pd.DataFrame(
    {
        "metric": [
            "total_checks",
            "passed_checks",
            "checks_requiring_review",
            "failed_checks"
        ],
        "value": [
            total_checks,
            passed_checks,
            check_items,
            failed_checks
        ]
    }
)


summary_file = (
    VALIDATION_DIR /
    "week03_validation_summary.csv"
)


summary.to_csv(
    summary_file,
    index=False
)


# ============================================================
# 21. FINAL OUTPUT
# ============================================================

print()
print("=" * 70)
print("WEEK 03 - DATA VALIDATION COMPLETE")
print("=" * 70)

print(f"Total checks: {total_checks}")
print(f"Passed checks: {passed_checks}")
print(f"Checks requiring review: {check_items}")
print(f"Failed checks: {failed_checks}")

print()
print(
    f"Validation report saved: "
    f"{validation_report_file}"
)

print(
    f"Validation summary saved: "
    f"{summary_file}"
)

print()
print(
    "All data validation and consistency checks completed."
)