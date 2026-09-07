import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Inventory Level Forecasting
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

# Load stock ledger
stock_ledger = pd.read_csv(
    DATA_DIR / "stock_ledger.csv"
)

# Select required columns
stock_ledger = stock_ledger[[
    "product_id",
    "branch_id",
    "movement_date",
    "quantity",
    "movement_type",
    "running_balance"
]]

# Convert date
stock_ledger["movement_date"] = pd.to_datetime(
    stock_ledger["movement_date"],
    errors="coerce"
)

# Remove invalid records
stock_ledger = stock_ledger.dropna(
    subset=[
        "movement_date",
        "product_id",
        "branch_id",
        "running_balance"
    ]
)

# Keep date only
stock_ledger["movement_date"] = (
    stock_ledger["movement_date"].dt.normalize()
)

# Sort data
stock_ledger = stock_ledger.sort_values(
    ["product_id", "branch_id", "movement_date"]
)

# --------------------------------------------------
# Create daily inventory levels
# --------------------------------------------------

daily_inventory = []

for (product_id, branch_id), group in stock_ledger.groupby(
    ["product_id", "branch_id"]
):

    group = (
        group
        .sort_values("movement_date")
        .drop_duplicates(
            subset=["movement_date"],
            keep="last"
        )
    )

    date_range = pd.date_range(
        start=group["movement_date"].min(),
        end=group["movement_date"].max(),
        freq="D"
    )

    daily_group = pd.DataFrame({
        "product_id": product_id,
        "branch_id": branch_id,
        "movement_date": date_range
    })

    daily_group = daily_group.merge(
        group[[
            "movement_date",
            "quantity",
            "movement_type",
            "running_balance"
        ]],
        on="movement_date",
        how="left"
    )

    # Carry forward the latest inventory balance
    daily_group["running_balance"] = (
        daily_group["running_balance"]
        .ffill()
    )

    # No movement on a day = zero movement
    daily_group["quantity"] = (
        daily_group["quantity"]
        .fillna(0)
    )

    daily_group["movement_type"] = (
        daily_group["movement_type"]
        .fillna("No Movement")
    )

    daily_inventory.append(daily_group)

stock_ledger = pd.concat(
    daily_inventory,
    ignore_index=True
)

# Sort final daily data
stock_ledger = stock_ledger.sort_values(
    ["product_id", "branch_id", "movement_date"]
)

# --------------------------------------------------
# Calculate calendar-day rolling inventory averages
# --------------------------------------------------

stock_ledger["7_day_avg_inventory"] = (
    stock_ledger
    .groupby(
        ["product_id", "branch_id"]
    )["running_balance"]
    .transform(
        lambda x: x.rolling(
            window=7,
            min_periods=1
        ).mean()
    )
)

stock_ledger["30_day_avg_inventory"] = (
    stock_ledger
    .groupby(
        ["product_id", "branch_id"]
    )["running_balance"]
    .transform(
        lambda x: x.rolling(
            window=30,
            min_periods=1
        ).mean()
    )
)

# --------------------------------------------------
# Forecast next inventory level
# --------------------------------------------------

stock_ledger["next_inventory_forecast"] = (
    stock_ledger["7_day_avg_inventory"]
)

# Round forecast values
stock_ledger["7_day_avg_inventory"] = (
    stock_ledger["7_day_avg_inventory"].round(2)
)

stock_ledger["30_day_avg_inventory"] = (
    stock_ledger["30_day_avg_inventory"].round(2)
)

stock_ledger["next_inventory_forecast"] = (
    stock_ledger["next_inventory_forecast"].round(2)
)

# Save output
output_file = (
    OUTPUT_DIR / "inventory_level_forecasting.csv"
)

stock_ledger.to_csv(
    output_file,
    index=False
)

print(
    "Inventory Level Forecasting completed successfully."
)
print(f"Output saved to: {output_file}")
print(
    f"Records generated: {len(stock_ledger)}"
)