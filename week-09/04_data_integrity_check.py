import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# WEEK 09 - DATA INTEGRITY & ERROR DETECTION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "week-09" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def find_csv(filename):
    matches = list(BASE_DIR.rglob(filename))
    if matches:
        return matches[0]
    return None


# ------------------------------------------------------------
# 1. Load Stock Ledger
# ------------------------------------------------------------

stock_file = find_csv("stock_ledger.csv")

if stock_file is None:
    print("ERROR: stock_ledger.csv not found.")
    raise SystemExit(1)

df = pd.read_csv(stock_file)

print("=" * 60)
print("WEEK 09 - DATA INTEGRITY & ERROR DETECTION")
print("=" * 60)

print(f"\nDataset: {stock_file}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# ------------------------------------------------------------
# 2. Missing Value Check
# ------------------------------------------------------------

missing_values = df.isnull().sum()

missing_percentage = (
    missing_values / len(df) * 100
    if len(df) > 0
    else 0
)


# ------------------------------------------------------------
# 3. Duplicate Record Check
# ------------------------------------------------------------

duplicate_count = df.duplicated().sum()


# ------------------------------------------------------------
# 4. Empty String Check
# ------------------------------------------------------------

empty_string_counts = {}

for col in df.select_dtypes(include="object").columns:

    count = (
        df[col]
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    empty_string_counts[col] = count


# ------------------------------------------------------------
# 5. Negative Numeric Value Check
# ------------------------------------------------------------

numeric_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

negative_counts = {}

for col in numeric_columns:
    negative_counts[col] = (
        df[col] < 0
    ).sum()


# ------------------------------------------------------------
# 6. Build Data Quality Report
# ------------------------------------------------------------

quality_report = pd.DataFrame({
    "column_name": df.columns,
    "data_type": [
        str(df[col].dtype)
        for col in df.columns
    ],
    "total_records": len(df),
    "missing_count": [
        int(missing_values[col])
        for col in df.columns
    ],
    "missing_percentage": [
        round(float(missing_percentage[col]), 2)
        for col in df.columns
    ],
    "empty_string_count": [
        int(empty_string_counts.get(col, 0))
        for col in df.columns
    ],
    "negative_value_count": [
        int(negative_counts.get(col, 0))
        for col in df.columns
    ],
    "unique_values": [
        int(df[col].nunique(dropna=True))
        for col in df.columns
    ]
})


# ------------------------------------------------------------
# 7. Column-level Error Status
# ------------------------------------------------------------

def determine_status(row):

    if row["missing_count"] > 0:
        return "Review Required"

    if row["empty_string_count"] > 0:
        return "Review Required"

    return "OK"


quality_report["data_quality_status"] = (
    quality_report.apply(
        determine_status,
        axis=1
    )
)


# ------------------------------------------------------------
# 8. Overall Data Quality Summary
# ------------------------------------------------------------

total_cells = df.shape[0] * df.shape[1]

total_missing = int(
    df.isnull().sum().sum()
)

total_empty_strings = int(
    sum(empty_string_counts.values())
)

total_negative_values = int(
    sum(negative_counts.values())
)

duplicate_records = int(
    duplicate_count
)

error_columns = int(
    (
        quality_report["data_quality_status"]
        == "Review Required"
    ).sum()
)


# ------------------------------------------------------------
# 9. Overall Integrity Status
# ------------------------------------------------------------

if (
    total_missing == 0
    and total_empty_strings == 0
    and duplicate_records == 0
):
    overall_status = "PASS"
else:
    overall_status = "REVIEW REQUIRED"


# ------------------------------------------------------------
# 10. Save Data Quality Report
# ------------------------------------------------------------

output_file = OUTPUT_DIR / "data_integrity_report.csv"

quality_report.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# 11. Save Summary
# ------------------------------------------------------------

summary = pd.DataFrame({
    "metric": [
        "Total Records",
        "Total Columns",
        "Total Cells",
        "Missing Values",
        "Empty String Values",
        "Duplicate Records",
        "Negative Numeric Values",
        "Columns Requiring Review",
        "Overall Data Integrity Status"
    ],
    "value": [
        len(df),
        len(df.columns),
        total_cells,
        total_missing,
        total_empty_strings,
        duplicate_records,
        total_negative_values,
        error_columns,
        overall_status
    ]
})

summary_file = OUTPUT_DIR / "data_integrity_summary.csv"

summary.to_csv(
    summary_file,
    index=False
)


# ------------------------------------------------------------
# 12. Display Results
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATA INTEGRITY SUMMARY")
print("=" * 60)

print(f"Total records          : {len(df):,}")
print(f"Total columns          : {len(df.columns):,}")
print(f"Total cells            : {total_cells:,}")
print(f"Missing values         : {total_missing:,}")
print(f"Empty string values    : {total_empty_strings:,}")
print(f"Duplicate records      : {duplicate_records:,}")
print(f"Negative numeric values: {total_negative_values:,}")
print(f"Columns requiring review: {error_columns:,}")

print(f"\nOverall status         : {overall_status}")

print("\nOutput files saved:")
print(output_file)
print(summary_file)

print("\nWeek 09 data integrity check completed successfully.")