import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load CLV data
clv = pd.read_csv(
    OUTPUT_DIR / "customer_lifetime_value.csv"
)

# ---------------------------------------------------------
# HIGH-VALUE CUSTOMER THRESHOLD
# ---------------------------------------------------------
high_value_threshold = (
    clv["estimated_3_year_clv"].quantile(0.80)
)

clv["is_high_value_customer"] = (
    clv["estimated_3_year_clv"]
    >= high_value_threshold
)

# ---------------------------------------------------------
# CUSTOMER RANK
# ---------------------------------------------------------
clv["value_rank"] = (
    clv["estimated_3_year_clv"]
    .rank(
        method="dense",
        ascending=False
    )
    .astype(int)
)

# ---------------------------------------------------------
# VALUE CATEGORY
# ---------------------------------------------------------
clv["value_category"] = "Standard"

clv.loc[
    clv["is_high_value_customer"],
    "value_category"
] = "High Value"

# ---------------------------------------------------------
# SORT CUSTOMERS
# ---------------------------------------------------------
high_value_customers = clv.sort_values(
    by="estimated_3_year_clv",
    ascending=False
)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------
total_customers = len(clv)

high_value_count = (
    clv["is_high_value_customer"].sum()
)

high_value_percentage = (
    high_value_count
    / total_customers
    * 100
)

total_clv = (
    clv["estimated_3_year_clv"].sum()
)

high_value_clv = (
    clv.loc[
        clv["is_high_value_customer"],
        "estimated_3_year_clv"
    ].sum()
)

summary = pd.DataFrame({
    "metric": [
        "Total Customers",
        "High-Value Customers",
        "High-Value Customer Percentage",
        "High-Value CLV Threshold",
        "Total Estimated 3-Year CLV",
        "High-Value Customer CLV"
    ],
    "value": [
        total_customers,
        int(high_value_count),
        round(high_value_percentage, 2),
        round(high_value_threshold, 2),
        round(total_clv, 2),
        round(high_value_clv, 2)
    ]
})

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("HIGH-VALUE CUSTOMER IDENTIFICATION")
print("=" * 70)

print("\nHigh-Value Customer Threshold:")
print(round(high_value_threshold, 2))

print("\nTop High-Value Customers:")

print(
    high_value_customers[
        [
            "customer_id",
            "total_revenue",
            "estimated_3_year_clv",
            "clv_segment",
            "is_high_value_customer",
            "value_rank",
            "value_category"
        ]
    ].head(20).to_string(index=False)
)

print("\nHigh-Value Customer Summary:")

print(
    summary.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------------
customer_output = (
    OUTPUT_DIR / "high_value_customer_identification.csv"
)

summary_output = (
    OUTPUT_DIR / "high_value_customer_summary.csv"
)

high_value_customers.to_csv(
    customer_output,
    index=False
)

summary.to_csv(
    summary_output,
    index=False
)

print("\n" + "=" * 70)
print("High-Value Customer Identification completed successfully.")
print(f"Customer output saved to: {customer_output}")
print(f"Summary output saved to: {summary_output}")
print("=" * 70)