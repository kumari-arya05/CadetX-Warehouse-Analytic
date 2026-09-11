import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="CadetX Warehouse Dashboard",
    page_icon="📦",
    layout="wide"
)

DATA_DIR = Path(__file__).parent.parent / "data"

st.title("📦 CadetX Warehouse Analytics Dashboard")
st.write("Week 10: Inventory, Shrinkage and Operational Risk Analysis")

files = list(DATA_DIR.glob("*.csv"))

if not files:
    st.error("No CSV files found in week-10/data folder.")
    st.stop()

dataframes = {}

for file in files:
    try:
        dataframes[file.stem] = pd.read_csv(file)
    except Exception as error:
        st.warning(f"Could not read {file.name}: {error}")

st.sidebar.header("Dashboard Filters")

selected_file = st.sidebar.selectbox(
    "Select Dataset",
    list(dataframes.keys())
)

df = dataframes[selected_file]

st.subheader(f"Dataset: {selected_file}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rows", len(df))

with col2:
    st.metric("Total Columns", len(df.columns))

with col3:
    st.metric("Missing Values", int(df.isnull().sum().sum()))

st.divider()

st.subheader("Data Preview")
st.dataframe(df, use_container_width=True)

st.subheader("Column Summary")

summary = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str).values,
    "Missing Values": df.isnull().sum().values,
    "Unique Values": df.nunique().values
})

st.dataframe(summary, use_container_width=True)

st.success("Week-10 dashboard loaded successfully!")