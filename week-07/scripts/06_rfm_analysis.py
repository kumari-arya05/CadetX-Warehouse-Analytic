import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# LOAD SALES DATA
# ---------------------------------------------------------
sales_orders = pd.read_csv(
    DATA_DIR / "sales_orders_header.csv"
)

sales_orders["order_date"] = pd.to_datetime(
    sales_orders["order_date"],
    errors="coerce"
)

sales_orders = sales_orders.dropna(
    subset=["customer_id", "order_date"]
)

# ---------------------------------------------------------
# SET ANALYSIS DATE
# ---------------------------------------------------------
analysis_date = sales_orders["order_date"].max() + pd.Timedelta(days=1)

# ---------------------------------------------------------
# RFM CALCULATION
# ---------------------------------------------------------
rfm = (
    sales_orders
    .groupby("customer_id")
    .agg(
        last_purchase_date=("order_date", "max"),
        frequency=("so_id", "count"),
        monetary=("total_order_value", "sum")
    )
    .reset_index()
)

# ---------------------------------------------------------
# RECENCY
# ---------------------------------------------------------
rfm["recency"] = (
    analysis_date - rfm["last_purchase_date"]
).dt.days

# ---------------------------------------------------------
# RFM SCORES
# ---------------------------------------------------------
rfm["recency_score"] = pd.qcut(
    rfm["recency"],
    q=4,
    labels=[4, 3, 2, 1],
    duplicates="drop"
).astype(int)

rfm["frequency_score"] = pd.qcut(
    rfm["frequency"].rank(method="first"),
    q=4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["monetary_score"] = pd.qcut(
    rfm["monetary"].rank(method="first"),
    q=4,
    labels=[1, 2, 3, 4]
).astype(int)

# ---------------------------------------------------------
# RFM TOTAL SCORE
# ---------------------------------------------------------
rfm["rfm_score"] = (
    rfm["recency_score"]
    + rfm["frequency_score"]
    + rfm["monetary_score"]
)

# ---------------------------------------------------------
# CUSTOMER SEGMENTS
# ---------------------------------------------------------
def customer_segment(score):
    if score >= 10:
        return "Champions"
    elif score >= 8:
        return "Loyal Customers"
    elif score >= 6:
        return "Potential Loyalists"
    elif score >= 4:
        return "At Risk"
    else:
        return "Lost Customers"


rfm["customer_segment"] = (
    rfm["rfm_score"]
    .apply(customer_segment)
)

# ---------------------------------------------------------
# ROUND MONETARY VALUES
# ---------------------------------------------------------
rfm["monetary"] = rfm["monetary"].round(2)

# ---------------------------------------------------------
# SORT RESULTS
# ---------------------------------------------------------
rfm = rfm.sort_values(
    by="rfm_score",
    ascending=False
)

# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("=" * 70)
print("RFM CUSTOMER ANALYSIS")
print("=" * 70)

print("\nRFM Analysis:")

print(
    rfm.head(20).to_string(index=False)
)

# ---------------------------------------------------------
# SEGMENT SUMMARY
# ---------------------------------------------------------
segment_summary = (
    rfm
    .groupby("customer_segment")
    .agg(
        customers=("customer_id", "nunique"),
        average_recency=("recency", "mean"),
        average_frequency=("frequency", "mean"),
        total_monetary=("monetary", "sum"),
        average_rfm_score=("rfm_score", "mean")
    )
    .reset_index()
)

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

print("\nRFM Segment Summary:")

print(
    segment_summary.to_string(index=False)
)

# ---------------------------------------------------------
# SAVE OUTPUTS
# ---------------------------------------------------------
rfm_output = OUTPUT_DIR / "rfm_analysis.csv"

summary_output = OUTPUT_DIR / "rfm_segment_summary.csv"

rfm.to_csv(
    rfm_output,
    index=False
)

segment_summary.to_csv(
    summary_output,
    index=False
)

# ---------------------------------------------------------
# SUCCESS MESSAGE
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("RFM Analysis completed successfully.")
print(f"RFM output saved to: {rfm_output}")
print(f"Summary output saved to: {summary_output}")
print("=" * 70)