# ============================================================
# CadetX Warehouse Analytics
# Week 04 — Warehouse Operations & Efficiency Analytics
# Step 08 — Warehouse Utilisation Benchmarking
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# 1. Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
FEATURES_DIR = DATA_DIR / "features"

PERFORMANCE_FILE = (
    FEATURES_DIR / "warehouse_performance.csv"
)

CAPACITY_FILE = (
    FEATURES_DIR / "warehouse_capacity_analysis.csv"
)

THROUGHPUT_FILE = (
    FEATURES_DIR / "warehouse_throughput.csv"
)

OUTPUT_FILE = (
    FEATURES_DIR / "warehouse_utilisation_benchmark.csv"
)


# ------------------------------------------------------------
# 2. Load Analysis Outputs
# ------------------------------------------------------------

print("=" * 70)
print("WEEK 04 — WAREHOUSE UTILISATION BENCHMARKING")
print("=" * 70)

performance = pd.read_csv(PERFORMANCE_FILE)
capacity = pd.read_csv(CAPACITY_FILE)
throughput = pd.read_csv(THROUGHPUT_FILE)

print(f"\nPerformance data : {performance.shape}")
print(f"Capacity data    : {capacity.shape}")
print(f"Throughput data  : {throughput.shape}")


# ------------------------------------------------------------
# 3. Validate Required Columns
# ------------------------------------------------------------

performance_columns = [
    "branch_id",
    "branch_name",
    "city",
    "state",
    "region",
    "warehouse_type",
    "performance_score",
    "performance_category",
]

capacity_columns = [
    "branch_id",
    "warehouse_capacity",
    "total_current_stock",
    "capacity_utilisation_pct",
    "capacity_status",
    "capacity_risk_level",
]

throughput_columns = [
    "branch_id",
    "total_movements",
    "total_throughput",
    "unique_products_moved",
]

missing_performance = [
    column
    for column in performance_columns
    if column not in performance.columns
]

missing_capacity = [
    column
    for column in capacity_columns
    if column not in capacity.columns
]

missing_throughput = [
    column
    for column in throughput_columns
    if column not in throughput.columns
]

if missing_performance:
    raise ValueError(
        f"Missing performance columns: {missing_performance}"
    )

if missing_capacity:
    raise ValueError(
        f"Missing capacity columns: {missing_capacity}"
    )

if missing_throughput:
    raise ValueError(
        f"Missing throughput columns: {missing_throughput}"
    )

print("✓ Required columns validated")


# ------------------------------------------------------------
# 4. Prepare Numeric Columns
# ------------------------------------------------------------

performance_numeric = [
    "performance_score",
]

capacity_numeric = [
    "warehouse_capacity",
    "total_current_stock",
    "capacity_utilisation_pct",
]

throughput_numeric = [
    "total_movements",
    "total_throughput",
    "unique_products_moved",
]

for column in performance_numeric:
    performance[column] = pd.to_numeric(
        performance[column],
        errors="coerce"
    )

for column in capacity_numeric:
    capacity[column] = pd.to_numeric(
        capacity[column],
        errors="coerce"
    )

for column in throughput_numeric:
    throughput[column] = pd.to_numeric(
        throughput[column],
        errors="coerce"
    )


# ------------------------------------------------------------
# 5. Merge Warehouse Metrics
# ------------------------------------------------------------

benchmark = (
    performance[
        performance_columns
    ]
    .merge(
        capacity[
            capacity_columns
        ],
        on="branch_id",
        how="left",
        validate="one_to_one"
    )
    .merge(
        throughput[
            throughput_columns
        ],
        on="branch_id",
        how="left",
        validate="one_to_one"
    )
)


# ------------------------------------------------------------
# 6. Calculate Benchmark Metrics
# ------------------------------------------------------------

benchmark["throughput_per_movement"] = (
    benchmark["total_throughput"]
    / benchmark["total_movements"]
)

benchmark["stock_per_product"] = (
    benchmark["total_current_stock"]
    / benchmark["unique_products_moved"]
)

benchmark["capacity_per_product"] = (
    benchmark["warehouse_capacity"]
    / benchmark["unique_products_moved"]
)


# ------------------------------------------------------------
# 7. Handle Invalid Ratios
# ------------------------------------------------------------

ratio_columns = [
    "throughput_per_movement",
    "stock_per_product",
    "capacity_per_product",
]

for column in ratio_columns:
    benchmark[column] = (
        benchmark[column]
        .replace(
            [float("inf"), -float("inf")],
            pd.NA
        )
    )


# ------------------------------------------------------------
# 8. Benchmark Percentiles
# ------------------------------------------------------------

benchmark["utilisation_percentile"] = (
    benchmark["capacity_utilisation_pct"]
    .rank(pct=True)
    * 100
)

benchmark["throughput_percentile"] = (
    benchmark["total_throughput"]
    .rank(pct=True)
    * 100
)

benchmark["performance_percentile"] = (
    benchmark["performance_score"]
    .rank(pct=True)
    * 100
)


# ------------------------------------------------------------
# 9. Overall Benchmark Score
# ------------------------------------------------------------

benchmark["benchmark_score"] = (
    benchmark["utilisation_percentile"] * 0.35
    + benchmark["throughput_percentile"] * 0.35
    + benchmark["performance_percentile"] * 0.30
)


# ------------------------------------------------------------
# 10. Benchmark Category
# ------------------------------------------------------------

def classify_benchmark(score):

    if pd.isna(score):
        return "Unknown"

    if score >= 80:
        return "Top Benchmark"

    if score >= 60:
        return "Above Average"

    if score >= 40:
        return "Average"

    return "Below Average"


benchmark["benchmark_category"] = (
    benchmark["benchmark_score"]
    .apply(classify_benchmark)
)


# ------------------------------------------------------------
# 11. Benchmark Ranking
# ------------------------------------------------------------

benchmark["benchmark_rank"] = (
    benchmark["benchmark_score"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype("Int64")
)


# ------------------------------------------------------------
# 12. Utilisation Benchmark Status
# ------------------------------------------------------------

def classify_utilisation_benchmark(utilisation):

    if pd.isna(utilisation):
        return "Unknown"

    if utilisation > 100:
        return "Over Capacity"

    if utilisation >= 80:
        return "High Utilisation"

    if utilisation >= 50:
        return "Balanced Utilisation"

    return "Low Utilisation"


benchmark["utilisation_benchmark_status"] = (
    benchmark["capacity_utilisation_pct"]
    .apply(classify_utilisation_benchmark)
)


# ------------------------------------------------------------
# 13. Round Analytical Values
# ------------------------------------------------------------

round_columns = [
    "capacity_utilisation_pct",
    "throughput_per_movement",
    "stock_per_product",
    "capacity_per_product",
    "utilisation_percentile",
    "throughput_percentile",
    "performance_percentile",
    "benchmark_score",
]

benchmark[round_columns] = (
    benchmark[round_columns].round(2)
)


# ------------------------------------------------------------
# 14. Sort by Benchmark Rank
# ------------------------------------------------------------

benchmark = (
    benchmark
    .sort_values(
        "benchmark_score",
        ascending=False
    )
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 15. Save Output
# ------------------------------------------------------------

benchmark.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# 16. Summary
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("WAREHOUSE UTILISATION BENCHMARK SUMMARY")
print("-" * 70)

print(
    "\nWarehouses analysed:",
    benchmark["branch_id"].nunique()
)

print(
    "Average benchmark score:",
    round(
        benchmark["benchmark_score"].mean(),
        2
    )
)

print(
    "Highest benchmark score:",
    round(
        benchmark["benchmark_score"].max(),
        2
    )
)

print("\nBenchmark Categories:")
print(
    benchmark[
        "benchmark_category"
    ].value_counts()
)

print("\nUtilisation Benchmark Status:")
print(
    benchmark[
        "utilisation_benchmark_status"
    ].value_counts()
)


# ------------------------------------------------------------
# 17. Display Results
# ------------------------------------------------------------

display_columns = [
    "branch_id",
    "branch_name",
    "capacity_utilisation_pct",
    "total_throughput",
    "performance_score",
    "benchmark_score",
    "benchmark_category",
    "benchmark_rank",
]

print("\nWarehouse Benchmark Results:")

print(
    benchmark[
        display_columns
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 18. Completion
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✓ Step 08 completed successfully.")
print(f"✓ Output saved to: {OUTPUT_FILE}")
print("=" * 70)