from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[2]

KPI_FILE = BASE_DIR / "analysis" / "kpi" / "final_kpi_summary.csv"
INSIGHTS_FILE = BASE_DIR / "analysis" / "insights" / "final_insights.csv"

OUTPUT_DIR = Path(__file__).resolve().parent

kpi_df = pd.read_csv(KPI_FILE)
insights_df = pd.read_csv(INSIGHTS_FILE)

print("\nWeek 12 Final Dashboard")
print("=" * 50)

print("\nKPI Summary:")
print(kpi_df.to_string(index=False))

print("\nFinal Insights:")
print(insights_df.to_string(index=False))

kpi_df["Value"] = pd.to_numeric(kpi_df["Value"], errors="coerce")
kpi_df = kpi_df.dropna(subset=["Value"])

plt.figure(figsize=(14, 8))
plt.bar(kpi_df["KPI"], kpi_df["Value"])

plt.title("Week 12 Final KPI Dashboard")
plt.xlabel("KPI")
plt.ylabel("Value")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()

dashboard_file = OUTPUT_DIR / "week12_final_kpi_dashboard.png"

plt.savefig(
    dashboard_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

kpi_df.to_csv(
    OUTPUT_DIR / "week12_final_dashboard_data.csv",
    index=False
)

print("\n" + "=" * 50)
print("FINAL DASHBOARD CREATED SUCCESSFULLY")
print("=" * 50)
print(f"\nDashboard: {dashboard_file}")
print(f"Data: {OUTPUT_DIR / 'week12_final_dashboard_data.csv'}")
