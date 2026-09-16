from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "week-11" / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Purchase order files load करो
purchase_header = pd.read_csv(
    DATA_DIR / "purchase_orders_header.csv"
)

purchase_lines = pd.read_csv(
    DATA_DIR / "purchase_orders_lines.csv"
)


# दोनों files को po_id से join करो
merged_data = purchase_lines.merge(
    purchase_header[
        [
            "po_id",
            "supplier_id",
            "branch_id",
            "order_date",
            "po_status"
        ]
    ],
    on="po_id",
    how="left"
)


# Numeric columns को number में convert करो
merged_data["quantity"] = pd.to_numeric(
    merged_data["quantity"],
    errors="coerce"
).fillna(0)

merged_data["line_total"] = pd.to_numeric(
    merged_data["line_total"],
    errors="coerce"
).fillna(0)


# Supplier-wise summary बनाओ
supplier_dashboard = (
    merged_data.groupby("supplier_id")
    .agg(
        units_ordered=("quantity", "sum"),
        purchase_value=("line_total", "sum"),
        purchase_orders=("po_id", "nunique")
    )
    .reset_index()
)


# Highest purchase value पहले दिखेगा
supplier_dashboard = supplier_dashboard.sort_values(
    by="purchase_value",
    ascending=False
)


# CSV save करो
output_file = OUTPUT_DIR / "supplier_performance_dashboard.csv"

supplier_dashboard.to_csv(
    output_file,
    index=False
)


print("Supplier dashboard created successfully.")
print(output_file)