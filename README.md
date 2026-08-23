# CadetX Warehouse Analytics

## Project Overview

**CadetX Warehouse Analytics** is a data analytics project developed as part of the **CadetX Virtual Work Experience Program**.

The project focuses on analysing Heavy Supplier, Inventory, Warehouse, Sales, Purchase, and Customer datasets to establish a reliable data foundation and generate meaningful business insights.

The project follows a structured analytics workflow covering:

**Data Profiling → Data Cleaning → Data Standardization → Data Quality Validation → Business Analytics → KPI Development**

---

## Project Objectives

The main objectives of this project are to:

- Explore and understand warehouse and supply chain datasets.
- Profile datasets using Python and Pandas.
- Identify data-quality issues such as missing values and duplicates.
- Clean and standardize datasets.
- Validate data quality and consistency.
- Understand relationships between business datasets.
- Develop business-focused KPIs and analytical insights.
- Analyse sales, purchasing, inventory, supplier, and customer performance.

---

## Project Structure

```text
CadetX-Warehouse-Analytic/
│
├── .vscode/
│
├── data/
│   └── cleaned/
│
├── docs/
│   └── data_profiling_report.md
│
├── notebooks/
│   └── week01_data_profiling.py
│
├── src/
│   ├── data_cleaning.py
│   ├── data_type_standardization.py
│   ├── data_quality_validation.py
│   └── handle_missing_values.py
│
├── week-01/
│   └── README.md
│
└── README.md
```

---

## Weekly Progress

### Week 1 — Data Foundation & Exploration

**Status: Completed**

Week 1 focused on establishing the data foundation for the project.

### Work Completed

- Explored and profiled all **12 CSV datasets**.
- Reviewed dataset rows, columns, and data types.
- Checked missing values across datasets.
- Checked duplicate records.
- Performed data cleaning using Python and Pandas.
- Standardized date-related fields.
- Performed data-quality validation.
- Analysed missing values in `purchase_orders_header.csv`.
- Created cleaned datasets in the `data/cleaned/` directory.
- Documented data-quality findings and preparation activities.
- Published the completed work to GitHub.

### Key Finding

`purchase_orders_header.csv` contains:

- **24,000 total rows**
- **2,370 missing `received_date` values**
- **0 duplicate rows**

The missing `received_date` values were retained as blank because they may represent purchase orders that have not yet been received. Artificial dates were not introduced to avoid changing the meaning of the source data.

### Week 1 Documentation

Detailed Week 1 documentation is available here:

`week-01/README.md`

---

## Tools & Technologies

### Programming & Data Analysis

- Python
- Pandas

### Development

- Visual Studio Code

### Version Control

- Git
- GitHub

---

## Core Skills Demonstrated

- Data Profiling
- Data Cleaning
- Data Quality Validation
- Missing Value Analysis
- Duplicate Detection
- Data Type Standardization
- Exploratory Data Analysis
- Dataset Structure Analysis
- Documentation
- Version Control

---

## Project Roadmap

Future phases of the project will focus on:

- Identifying primary and foreign key relationships.
- Understanding relationships between datasets.
- Developing business KPIs.
- Analysing sales and purchase performance.
- Analysing inventory and stock levels.
- Evaluating supplier performance.
- Analysing customer purchasing behaviour.
- Creating analytical summaries and visualizations.
- Generating actionable business insights.

---

## Repository

**GitHub Repository:**

https://github.com/kumari-arya05/CadetX-Warehouse-Analytic

---

## Author

**Kumari Arya**

**Program:** CadetX Virtual Work Experience Program

**Project:** Warehouse & Supply Chain Analytics

**Current Phase:** Week 1 — Data Foundation & Exploration
