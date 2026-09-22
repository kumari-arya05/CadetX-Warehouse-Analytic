from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "analysis" / "insights" / "final_insights.csv"
OUTPUT_DIR = BASE_DIR / "recommendations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

recommendations = []

for _, row in df.iterrows():

    kpi = str(row["KPI"])
    value = row["Value"]

    if kpi == "Total Products":
        recommendation = "Maintain a structured product master and regularly review product-level performance."

    elif kpi == "Total Inventory Records":
        recommendation = "Monitor inventory records regularly to maintain accurate stock visibility and data quality."

    elif kpi == "Total Sales Order Lines":
        recommendation = "Use sales order trends to identify high-demand products and support inventory planning."

    elif kpi == "Total Suppliers":
        recommendation = "Monitor supplier performance and dependency to improve procurement reliability."

    elif kpi == "Total Branches":
        recommendation = "Compare branch-level performance to identify operational differences and improvement opportunities."

    elif kpi == "Total Customers":
        recommendation = "Use customer-level sales patterns to support segmentation and targeted business decisions."

    elif kpi == "Total Units Sold":
        recommendation = "Track unit sales trends to identify demand patterns and improve replenishment planning."

    elif kpi == "Total Sales Value":
        recommendation = "Monitor sales value regularly and connect revenue trends with product, customer, and branch performance."

    elif kpi == "Total Current Stock":
        recommendation = "Monitor current inventory against demand to reduce excess stock and potential stockout risk."

    else:
        recommendation = "Monitor this KPI regularly and use trend analysis to support operational decision-making."

    recommendations.append({
        "KPI": kpi,
        "Value": value,
        "Unit": row["Unit"],
        "Recommendation": recommendation
    })

recommendations_df = pd.DataFrame(recommendations)

output_file = OUTPUT_DIR / "final_recommendations.csv"

recommendations_df.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 60)
print("WEEK 12 RECOMMENDATIONS CREATED SUCCESSFULLY")
print("=" * 60)

print("\nRecommendations:")
print(recommendations_df.to_string(index=False))

print(f"\nOutput file: {output_file}")
