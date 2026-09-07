import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# LOAD CUSTOMER CHURN DATA
# ---------------------------------------------------------
churn = pd.read_csv(
    OUTPUT_DIR / "customer_churn_analysis.csv"
)

# ---------------------------------------------------------
# AT-RISK CUSTOMER IDENTIFICATION
# ---------------------------------------------------------
churn["is_at_risk_customer"] = (
    churn["days_since_last_purchase"] >= 90
)

# ---------------------------------------------------------
# RISK CATEGORY
# ---------------------------------------------------------
churn["risk_category"] = "Active"

churn.loc[
    churn["days_since_last_purchase"] >= 90,
    "risk_category"
] = "At Risk"

churn.loc[
    churn["days_since_last_purchase"] >= 180,
    "risk_category"
] = "Churned"

# ---------------------------------------------------------
# PRIORITY
# ---------------------------------------------------------
churn["priority"] = "Low"

churn.loc[
    churn["days_since_last_purchase"] >= 90,
    "priority"
] = "Medium"

churn.loc[
    churn["days_since_last_purchase"] >= 180,
    "priority"
] = "High"

# ---------------------------------------------------------
# SORT BY RISK
# ---------------------------------------------------------
at_risk_customers = churn.sort_values(
    by="days_since_last_purchase",
    ascending=False
)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------
total_customers = len(churn)

at_risk_count = (
    churn["is_at_risk_customer"].sum()
)

churned_count = (
    churn["risk_category"] == "Churned"
).sum()

at_risk_percentage = (
    at_risk_count
    / total_customers
    * 100
)

churned_percentage = (
    churned_count
    / total_customers
    * 100
)

summary = pd.DataFrame({
    "metric": [
        "Total Customers",
        "At-Risk Customers",
        "At-Risk Customer Percentage",
        "Churned Customers",
        "Churned Customer Percentage"
    ],
    "value": [
        total_customers,
        int(at_risk_count),
        round(at_risk_percentage, 2),
        int(churned_count),
        round(churned_percentage, 2)
    ]
})

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("AT-RISK CUSTOMER IDENTIFICATION")
print("=" * 70)

print("\nAt-Risk Customers:")

print(
    at_risk_customers[
        [
            "customer_id",
            "days_since_last_purchase",
            "churn_status",
            "risk_category",
            "priority"
        ]
    ].head(20).to_string(index=False)
)

print("\nAt-Risk Customer Summary:")

print(
    summary.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------------
customer_output = (
    OUTPUT_DIR / "at_risk_customer_identification.csv"
)

summary_output = (
    OUTPUT_DIR / "at_risk_customer_summary.csv"
)

at_risk_customers.to_csv(
    customer_output,
    index=False
)

summary.to_csv(
    summary_output,
    index=False
)

# ---------------------------------------------------------
# SUCCESS MESSAGE
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("At-Risk Customer Identification completed successfully.")
print(f"Customer output saved to: {customer_output}")
print(f"Summary output saved to: {summary_output}")
print("=" * 70)