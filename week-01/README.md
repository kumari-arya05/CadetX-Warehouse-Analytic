# CadetX Warehouse Analytics

## Week 1 — Data Foundation & Exploration

### Project Overview

This project is part of the **CadetX Virtual Work Experience Program**, focused on applying data analytics techniques to a Heavy Supplier, Inventory, Warehouse, Sales, Purchase, and Customer data environment.

Week 1 establishes the data foundation required for subsequent business analytics. The primary focus was on understanding the available datasets, profiling their structure, identifying data-quality issues, cleaning and standardizing the data, and validating the resulting datasets.

The objective was to prepare reliable and structured data for further analysis, KPI development, and business intelligence activities.

---

## 1. Project Objective

The objective of Week 1 was to:

- Understand the structure and characteristics of the available datasets.
- Profile all CSV files using Python and Pandas.
- Inspect rows, columns, column names, and data types.
- Identify missing values and duplicate records.
- Perform data cleaning and standardization.
- Validate data quality after the cleaning process.
- Investigate important data-quality exceptions.
- Preserve original datasets while creating cleaned versions.
- Establish a reliable data foundation for future analytics.

---

## 2. Dataset Overview

A total of **12 CSV datasets** were explored and processed during Week 1.

### Dataset Files

| Dataset | Purpose |
|---|---|
| `branches.csv` | Branch and location information |
| `customers.csv` | Customer-related information |
| `inventory_master.csv` | Inventory master data |
| `invoices.csv` | Invoice and billing information |
| `payments.csv` | Payment-related information |
| `products.csv` | Product master information |
| `purchase_orders_header.csv` | Purchase order header information |
| `purchase_orders_lines.csv` | Purchase order line-level information |
| `sales_orders_header.csv` | Sales order header information |
| `sales_orders_lines.csv` | Sales order line-level information |
| `stock_ledger.csv` | Inventory movement and stock ledger information |
| `suppliers.csv` | Supplier information |

These datasets provide the foundation for future analysis across procurement, inventory, sales, supplier performance, customer behaviour, and warehouse operations.

---

## 3. Week 1 Data Workflow

The Week 1 workflow followed a structured data-preparation process:

**Data Discovery → Data Profiling → Data Cleaning → Date Standardization → Data Quality Validation → Missing Value Analysis**

This workflow was designed to create consistent and analysis-ready datasets while preserving the original source data.

---

## 4. Data Profiling

Data profiling was performed using **Python and Pandas**.

### Profiling Activities

- Dataset file discovery
- Row and column count inspection
- Column name inspection
- Data type inspection
- Missing-value analysis
- Duplicate-row detection
- Initial record inspection
- Review of dataset structure and consistency

### Profiling Script

```text
notebooks/week01_data_profiling.py
