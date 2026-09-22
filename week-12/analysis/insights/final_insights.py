import pandas as pd
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Input KPI file
INPUT_FILE = (
    PROJECT_ROOT
    / "week-12"
    / "analysis"
    / "kpi"
    / "final_kpi_summary.csv"
)

# Output file
OUTPUT_DIR = PROJECT_ROOT / "week-12" / "analysis" / "insights"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "final_insights.csv"

# Read KPI data
df = pd.read_csv(INPUT_FILE)

insights = []

for _, row in df.iterrows():
    kpi = row["KPI"]
    value = row["Value"]
    unit = row["Unit"]

    if kpi == "Total Sales Value":
        insight = (
            f"Total sales value recorded is {value} {unit}, "
            "providing an overall view of business sales performance."
        )

    elif kpi == "Total Current Stock":
        insight = (
            f"Current inventory stands at {value} {unit}, "
            "indicating the total stock available across the warehouse network."
        )

    elif kpi == "Total Units Sold":
        insight = (
            f"Total units sold are {value} {unit}, "
            "representing overall sales volume."
        )

    elif kpi == "Total Suppliers":
        insight = (
            f"The business works with {value} suppliers, "
            "supporting procurement and supply operations."
        )

    elif kpi == "Total Branches":
        insight = (
            f"The analysis covers {value} branches, "
            "providing a multi-branch operational view."
        )

    elif kpi == "Total Customers":
        insight = (
            f"The dataset contains {value} customers, "
            "representing the customer base included in the analysis."
        )

    else:
        insight = f"{kpi}: {value} {unit}"

    insights.append({
        "KPI": kpi,
        "Value": value,
        "Unit": unit,
        "Insight": insight
    })

# Create final insights dataframe
final_insights = pd.DataFrame(insights)

# Save output
final_insights.to_csv(OUTPUT_FILE, index=False)

print("\nFinal Insights created successfully.")
print(f"Output file: {OUTPUT_FILE}")

print("\nFinal Insights:")
print(final_insights.to_string(index=False))