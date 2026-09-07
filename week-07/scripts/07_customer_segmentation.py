import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load RFM analysis
rfm = pd.read_csv(
    OUTPUT_DIR / "rfm_analysis.csv"
)

# Customer segmentation
def segment_customer(row):
    if row["rfm_score"] >= 10:
        return "Champions"
    elif row["rfm_score"] >= 8:
        return "Loyal Customers"
    elif row["rfm_score"] >= 6:
        return "Potential Loyalists"
    elif row["rfm_score"] >= 4:
        return "At Risk"
    else:
        return "Lost Customers"


rfm["customer_segment"] = rfm.apply(
    segment_customer,
    axis=1
)

# Segment summary
segment_summary = (
    rfm
    .groupby("customer_segment")
    .agg(
        customer_count=("customer_id", "nunique"),
        average_recency=("recency", "mean"),
        average_frequency=("frequency", "mean"),
        total_monetary=("monetary", "sum"),
        average_rfm_score=("rfm_score", "mean")
    )
    .reset_index()
)

# Round values
segment_summary["average_recency"] = (
    segment_summary["average_recency"].round(2)
)

segment_summary["average_frequency"] = (
    segment_summary["average_frequency"].round(2)
)

segment_summary["total_monetary"] = (
    segment_summary["total_monetary"].round(2)
)

segment_summary["average_rfm_score"] = (
    segment_summary["average_rfm_score"].round(2)
)

# Sort segments
segment_summary = segment_summary.sort_values(
    by="customer_count",
    ascending=False
)

# Display
print("=" * 70)
print("CUSTOMER SEGMENTATION")
print("=" * 70)

print("\nCustomer Segmentation:")
print(
    rfm[
        [
            "customer_id",
            "recency",
            "frequency",
            "monetary",
            "rfm_score",
            "customer_segment"
        ]
    ].head(20).to_string(index=False)
)

print("\nSegment Summary:")
print(
    segment_summary.to_string(index=False)
)

# Save outputs
customer_output = (
    OUTPUT_DIR / "customer_segmentation.csv"
)

summary_output = (
    OUTPUT_DIR / "customer_segment_summary.csv"
)

rfm.to_csv(
    customer_output,
    index=False
)

segment_summary.to_csv(
    summary_output,
    index=False
)

print("\n" + "=" * 70)
print("Customer Segmentation completed successfully.")
print(f"Customer output saved to: {customer_output}")
print(f"Summary output saved to: {summary_output}")
print("=" * 70)