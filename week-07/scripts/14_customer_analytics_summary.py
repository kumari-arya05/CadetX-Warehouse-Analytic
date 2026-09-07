import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# LOAD OUTPUT FILES
# ---------------------------------------------------------
purchase_behaviour = pd.read_csv(
    OUTPUT_DIR / "customer_purchase_behaviour.csv"
)

rfm = pd.read_csv(
    OUTPUT_DIR / "rfm_analysis.csv"
)

segmentation = pd.read_csv(
    OUTPUT_DIR / "customer_segmentation.csv"
)

clv = pd.read_csv(
    OUTPUT_DIR / "customer_lifetime_value.csv"
)

retention = pd.read_csv(
    OUTPUT_DIR / "customer_retention_analysis.csv"
)

churn = pd.read_csv(
    OUTPUT_DIR / "customer_churn_analysis.csv"
)

cohort = pd.read_csv(
    OUTPUT_DIR / "customer_cohort_analysis.csv"
)

high_value = pd.read_csv(
    OUTPUT_DIR / "high_value_customer_identification.csv"
)

at_risk = pd.read_csv(
    OUTPUT_DIR / "at_risk_customer_identification.csv"
)

# ---------------------------------------------------------
# CREATE SUMMARY
# ---------------------------------------------------------
summary_data = []

# Purchase Behaviour
summary_data.append({
    "analysis": "Customer Purchase Behaviour",
    "metric": "Total Customers",
    "value": purchase_behaviour["customer_id"].nunique()
})

summary_data.append({
    "analysis": "Customer Purchase Behaviour",
    "metric": "Total Orders",
    "value": purchase_behaviour["total_orders"].sum()
})

summary_data.append({
    "analysis": "Customer Purchase Behaviour",
    "metric": "Total Order Value",
    "value": round(
        purchase_behaviour["total_order_value"].sum(),
        2
    )
})

# RFM
summary_data.append({
    "analysis": "RFM Analysis",
    "metric": "Customers Analysed",
    "value": rfm["customer_id"].nunique()
})

summary_data.append({
    "analysis": "RFM Analysis",
    "metric": "RFM Segments",
    "value": rfm["customer_segment"].nunique()
})

# Segmentation
summary_data.append({
    "analysis": "Customer Segmentation",
    "metric": "Customers Segmented",
    "value": segmentation["customer_id"].nunique()
})

# CLV
summary_data.append({
    "analysis": "Customer Lifetime Value",
    "metric": "Customers Analysed",
    "value": clv["customer_id"].nunique()
})

summary_data.append({
    "analysis": "Customer Lifetime Value",
    "metric": "Total Estimated 3-Year CLV",
    "value": round(
        clv["estimated_3_year_clv"].sum(),
        2
    )
})

summary_data.append({
    "analysis": "Customer Lifetime Value",
    "metric": "Average Estimated 3-Year CLV",
    "value": round(
        clv["estimated_3_year_clv"].mean(),
        2
    )
})

# Retention
summary_data.append({
    "analysis": "Customer Retention",
    "metric": "Customers Analysed",
    "value": retention["customer_id"].nunique()
})

# Churn
summary_data.append({
    "analysis": "Customer Churn",
    "metric": "Customers Analysed",
    "value": churn["customer_id"].nunique()
})

summary_data.append({
    "analysis": "Customer Churn",
    "metric": "Churned Customers",
    "value": int(
        churn["is_churned"].sum()
    )
})

# Cohort
summary_data.append({
    "analysis": "Customer Cohort Analysis",
    "metric": "Cohort Records",
    "value": len(cohort)
})

# High Value
summary_data.append({
    "analysis": "High-Value Customer Identification",
    "metric": "High-Value Customers",
    "value": int(
        high_value["is_high_value_customer"].sum()
    )
})

# At Risk
summary_data.append({
    "analysis": "At-Risk Customer Identification",
    "metric": "At-Risk Customers",
    "value": int(
        at_risk["is_at_risk_customer"].sum()
    )
})

# ---------------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------------
summary = pd.DataFrame(summary_data)

# ---------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------
print("=" * 70)
print("CUSTOMER ANALYTICS SUMMARY")
print("=" * 70)

print(
    summary.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUT
# ---------------------------------------------------------
output_file = (
    OUTPUT_DIR / "customer_analytics_summary.csv"
)

summary.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 70)
print("Customer Analytics Summary completed successfully.")
print(f"Output saved to: {output_file}")
print("=" * 70)