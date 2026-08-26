# ============================================================
# CadetX Warehouse Analytics
# Week 04 — Warehouse Operations & Efficiency Analytics
# Step 07 — Operational Bottleneck Detection
# ============================================================

import pandas as pd
from pathlib import Path


# ------------------------------------------------------------
# 1. Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
FEATURES_DIR = DATA_DIR / "features"

PERFORMANCE_FILE = FEATURES_DIR / "warehouse_performance.csv"
CAPACITY_FILE = FEATURES_DIR / "warehouse_capacity_analysis.csv"
THROUGHPUT_FILE = FEATURES_DIR / "warehouse_throughput.csv"

OUTPUT_FILE = FEATURES_DIR / "warehouse_bottleneck_detection.csv"


# ------------------------------------------------------------
# 2. Load Analysis Outputs
# ------------------------------------------------------------

print("=" * 70)
print("WEEK 04 — OPERATIONAL BOTTLENECK DETECTION")
print("=" * 70)

performance = pd.read_csv(PERFORMANCE_FILE)
capacity = pd.read_csv(CAPACITY_FILE)
throughput = pd.read_csv(THROUGHPUT_FILE)

print(f"\nPerformance data: {performance.shape}")
print(f"Capacity data: {capacity.shape}")
print(f"Throughput data: {throughput.shape}")


# ------------------------------------------------------------
# 3. Validate Required Columns
# ------------------------------------------------------------

performance_columns = [
    "branch_id",
    "branch_name",
    "performance_score",
    "performance_category",
]

capacity_columns = [
    "branch_id",
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

numeric_columns = [
    "performance_score",
]

for column in numeric_columns:
    performance[column] = pd.to_numeric(
        performance[column],
        errors="coerce"
    )


capacity_numeric = [
    "capacity_utilisation_pct",
]

for column in capacity_numeric:
    capacity[column] = pd.to_numeric(
        capacity[column],
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
# 5. Merge Warehouse Metrics
# ------------------------------------------------------------

bottlenecks = (
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
# 6. Calculate Throughput Percentile
# ------------------------------------------------------------

bottlenecks["throughput_percentile"] = (
    bottlenecks["total_throughput"]
    .rank(
        pct=True
    )
    * 100
)


# ------------------------------------------------------------
# 7. Capacity Pressure Flag
# ------------------------------------------------------------

bottlenecks["capacity_pressure_flag"] = (
    bottlenecks["capacity_utilisation_pct"] >= 80
)


# ------------------------------------------------------------
# 8. High Throughput Flag
# ------------------------------------------------------------

throughput_threshold = (
    bottlenecks["total_throughput"].quantile(0.75)
)

bottlenecks["high_throughput_flag"] = (
    bottlenecks["total_throughput"]
    >= throughput_threshold
)


# ------------------------------------------------------------
# 9. Low Performance Flag
# ------------------------------------------------------------

bottlenecks["low_performance_flag"] = (
    bottlenecks["performance_score"] < 60
)


# ------------------------------------------------------------
# 10. Bottleneck Indicator Count
# ------------------------------------------------------------

bottlenecks["bottleneck_indicator_count"] = (
    bottlenecks["capacity_pressure_flag"].astype(int)
    + bottlenecks["high_throughput_flag"].astype(int)
    + bottlenecks["low_performance_flag"].astype(int)
)


# ------------------------------------------------------------
# 11. Bottleneck Classification
# ------------------------------------------------------------

def classify_bottleneck(row):

    indicators = row["bottleneck_indicator_count"]

    if indicators >= 3:
        return "Critical Bottleneck"

    if indicators == 2:
        return "Potential Bottleneck"

    if indicators == 1:
        return "Monitor"

    return "No Bottleneck"


bottlenecks["bottleneck_status"] = (
    bottlenecks.apply(
        classify_bottleneck,
        axis=1
    )
)


# ------------------------------------------------------------
# 12. Bottleneck Reason
# ------------------------------------------------------------

def identify_reason(row):

    reasons = []

    if row["capacity_pressure_flag"]:
        reasons.append("High Capacity Utilisation")

    if row["high_throughput_flag"]:
        reasons.append("High Throughput")

    if row["low_performance_flag"]:
        reasons.append("Low Performance")

    if not reasons:
        return "No Major Bottleneck Indicator"

    return "; ".join(reasons)


bottlenecks["bottleneck_reason"] = (
    bottlenecks.apply(
        identify_reason,
        axis=1
    )
)


# ------------------------------------------------------------
# 13. Bottleneck Priority
# ------------------------------------------------------------

def classify_priority(status):

    if status == "Critical Bottleneck":
        return "High"

    if status == "Potential Bottleneck":
        return "Medium"

    if status == "Monitor":
        return "Low"

    return "Normal"


bottlenecks["action_priority"] = (
    bottlenecks["bottleneck_status"]
    .apply(classify_priority)
)


# ------------------------------------------------------------
# 14. Round Values
# ------------------------------------------------------------

bottlenecks[
    "throughput_percentile"
] = (
    bottlenecks[
        "throughput_percentile"
    ].round(2)
)


# ------------------------------------------------------------
# 15. Sort by Bottleneck Severity
# ------------------------------------------------------------

status_order = {
    "Critical Bottleneck": 1,
    "Potential Bottleneck": 2,
    "Monitor": 3,
    "No Bottleneck": 4,
}

bottlenecks["status_order"] = (
    bottlenecks["bottleneck_status"]
    .map(status_order)
)

bottlenecks = (
    bottlenecks
    .sort_values(
        [
            "status_order",
            "performance_score",
        ],
        ascending=[True, True]
    )
    .drop(columns="status_order")
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 16. Save Output
# ------------------------------------------------------------

bottlenecks.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# 17. Summary
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("BOTTLENECK DETECTION SUMMARY")
print("-" * 70)

print(
    "\nWarehouses analysed:",
    bottlenecks["branch_id"].nunique()
)

print("\nBottleneck Status:")
print(
    bottlenecks[
        "bottleneck_status"
    ].value_counts()
)

print("\nAction Priority:")
print(
    bottlenecks[
        "action_priority"
    ].value_counts()
)

print(
    "\nHigh throughput threshold:",
    round(throughput_threshold, 2)
)


# ------------------------------------------------------------
# 18. Display Results
# ------------------------------------------------------------

display_columns = [
    "branch_id",
    "branch_name",
    "capacity_utilisation_pct",
    "total_throughput",
    "performance_score",
    "bottleneck_indicator_count",
    "bottleneck_status",
    "bottleneck_reason",
    "action_priority",
]

print("\nWarehouse Bottleneck Results:")

print(
    bottlenecks[
        display_columns
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 19. Completion
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("✓ Step 07 completed successfully.")
print(f"✓ Output saved to: {OUTPUT_FILE}")
print("=" * 70)