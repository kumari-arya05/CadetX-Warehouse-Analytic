# ============================================================
# CadetX Warehouse Analytics
# Week 04 — Warehouse Operations & Efficiency Analytics
# Step 06 — Warehouse Performance Scoring
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# 1. Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
FEATURES_DIR = DATA_DIR / "features"

UTILISATION_FILE = (
    FEATURES_DIR / "warehouse_space_utilisation.csv"
)

THROUGHPUT_FILE = (
    FEATURES_DIR / "warehouse_throughput.csv"
)

OUTPUT_FILE = (
    FEATURES_DIR / "warehouse_performance.csv"
)


# ------------------------------------------------------------
# 2. Load Analysis Outputs
# ------------------------------------------------------------

print("=" * 70)
print("WEEK 04 — WAREHOUSE PERFORMANCE SCORING")
print("=" * 70)

utilisation = pd.read_csv(
    UTILISATION_FILE
)

throughput = pd.read_csv(
    THROUGHPUT_FILE
)

print(
    f"\nUtilisation data: {utilisation.shape}"
)

print(
    f"Throughput data: {throughput.shape}"
)


# ------------------------------------------------------------
# 3. Select Required Columns
# ------------------------------------------------------------

utilisation_columns = [
    "branch_id",
    "branch_name",
    "city",
    "state",
    "region",
    "warehouse_type",
    "warehouse_capacity",
    "total_current_stock",
    "capacity_utilisation_pct",
    "utilisation_status",
]

throughput_columns = [
    "branch_id",
    "total_movements",
    "total_throughput",
    "unique_products_moved",
]


# ------------------------------------------------------------
# 4. Validate Columns
# ------------------------------------------------------------

missing_utilisation = [
    column
    for column in utilisation_columns
    if column not in utilisation.columns
]

missing_throughput = [
    column
    for column in throughput_columns
    if column not in throughput.columns
]

if missing_utilisation:
    raise ValueError(
        f"Missing utilisation columns: {missing_utilisation}"
    )

if missing_throughput:
    raise ValueError(
        f"Missing throughput columns: {missing_throughput}"
    )

print("✓ Required columns validated")


# ------------------------------------------------------------
# 5. Prepare Numeric Fields
# ------------------------------------------------------------

numeric_columns = [
    "warehouse_capacity",
    "total_current_stock",
    "capacity_utilisation_pct",
]

for column in numeric_columns:
    utilisation[column] = pd.to_numeric(
        utilisation[column],
        errors="coerce"
    )


throughput_numeric = [
    "total_movements",
    "total_throughput",
    "unique_products_moved",
]

for column in throughput_numeric:
    throughput[column] = pd.to_numeric(
        throughput[column],
        errors="coerce"
    )


# ------------------------------------------------------------
# 6. Merge Warehouse Metrics
# ------------------------------------------------------------

performance = utilisation[
    utilisation_columns
].merge(
    throughput[
        throughput_columns
    ],
    on="branch_id",
    how="left",
    validate="one_to_one"
)


# ------------------------------------------------------------
# 7. Handle Missing Throughput Values
# ------------------------------------------------------------

for column in throughput_numeric:
    performance[column] = (
        performance[column]
        .fillna(0)
    )


# ------------------------------------------------------------
# 8. Calculate Utilisation Score
# ------------------------------------------------------------

performance["utilisation_score"] = (
    performance["capacity_utilisation_pct"]
    .clip(lower=0, upper=100)
)


# ------------------------------------------------------------
# 9. Calculate Throughput Score
# ------------------------------------------------------------

max_throughput = (
    performance["total_throughput"].max()
)

if pd.isna(max_throughput) or max_throughput == 0:
    performance["throughput_score"] = 0
else:
    performance["throughput_score"] = (
        performance["total_throughput"]
        / max_throughput
    ) * 100


# ------------------------------------------------------------
# 10. Calculate Product Coverage Score
# ------------------------------------------------------------

max_products = (
    performance["unique_products_moved"].max()
)

if pd.isna(max_products) or max_products == 0:
    performance["product_coverage_score"] = 0
else:
    performance["product_coverage_score"] = (
        performance["unique_products_moved"]
        / max_products
    ) * 100


# ------------------------------------------------------------
# 11. Warehouse Performance Score
# ------------------------------------------------------------

performance["performance_score"] = (
    performance["utilisation_score"] * 0.40
    + performance["throughput_score"] * 0.40
    + performance["product_coverage_score"] * 0.20
)


# ------------------------------------------------------------
# 12. Performance Classification
# ------------------------------------------------------------

def classify_performance(score):

    if pd.isna(score):
        return "Unknown"

    if score >= 80:
        return "High Performance"

    if score >= 60:
        return "Good Performance"

    if score >= 40:
        return "Moderate Performance"

    return "Low Performance"


performance["performance_category"] = (
    performance["performance_score"]
    .apply(classify_performance)
)


# ------------------------------------------------------------
# 13. Performance Ranking
# ------------------------------------------------------------

performance["performance_rank"] = (
    performance["performance_score"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype("Int64")
)


# ------------------------------------------------------------
# 14. Round Scores
# ------------------------------------------------------------

score_columns = [
    "utilisation_score",
    "throughput_score",
    "product_coverage_score",
    "performance_score",
]

performance[score_columns] = (
    performance[score_columns]
    .round(2)
)


# ------------------------------------------------------------
# 15. Sort by Performance
# ------------------------------------------------------------

performance = (
    performance
    .sort_values(
        "performance_score",
        ascending=False
    )
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 16. Save Output
# ------------------------------------------------------------

performance.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# 17. Summary
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("WAREHOUSE PERFORMANCE SUMMARY")
print("-" * 70)

print(
    "\nWarehouses analysed:",
    performance["branch_id"].nunique()
)

print(
    "Average performance score:",
    round(
        performance["performance_score"].mean(),
        2
    )
)

print(
    "Highest performance score:",
    round(
        performance["performance_score"].max(),
        2
    )
)

print("\nPerformance Categories:")
print(
    performance[
        "performance_category"
    ].value_counts()
)


# ------------------------------------------------------------
# 18. Display Results
# ------------------------------------------------------------

display_columns = [
    "branch_id",
    "branch_name",
    "capacity_utilisation_pct",
    "total_throughput",
    "unique_products_moved",
    "utilisation_score",
    "throughput_score",
    "product_coverage_score",
    "performance_score",
    "performance_category",
    "performance_rank",
]

print("\nWarehouse Performance Results:")

print(
    performance[
        display_columns
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 19. Completion
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✓ Step 06 completed successfully.")
print(f"✓ Output saved to: {OUTPUT_FILE}")
print("=" * 70)