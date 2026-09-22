import pandas as pd
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Input file from Week 11
INPUT_FILE = PROJECT_ROOT / "week-11" / "outputs" / "week11_kpi_summary.csv"

# Output folder
OUTPUT_DIR = PROJECT_ROOT / "week-12" / "analysis" / "kpi"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Output file
OUTPUT_FILE = OUTPUT_DIR / "final_kpi_summary.csv"

# Check input file
if not INPUT_FILE.exists():
    print("ERROR: Week 11 KPI file not found.")
    print(INPUT_FILE)
    raise SystemExit(1)

# Read Week 11 KPI data
df = pd.read_csv(INPUT_FILE)

# Keep the actual KPI structure
final_kpi = df[["KPI", "Value", "Unit"]].copy()

# Add source information
final_kpi.insert(0, "Source", "Week 11 KPI Summary")

# Save final KPI summary
final_kpi.to_csv(OUTPUT_FILE, index=False)

print("\nWeek 12 Final KPI Summary created successfully.")
print(f"Output file: {OUTPUT_FILE}")

print("\nFinal KPI Summary:")
print(final_kpi.to_string(index=False))