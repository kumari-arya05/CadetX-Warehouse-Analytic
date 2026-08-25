# CadetX Warehouse Analytics

## Project Overview

**CadetX Warehouse Analytics** is a data analytics project developed as part of the **CadetX Virtual Work Experience Program**.

The project focuses on analysing Heavy Supplier, Inventory, Warehouse, Sales, Purchase, and Customer datasets to establish a reliable data foundation and generate meaningful business insights.

The project follows a structured analytics workflow:

**Data Profiling → Data Cleaning → Data Standardization → Data Integration → Data Validation → Feature Engineering → KPI Development**

---

## Project Objectives

The main objectives of this project are to:

- Explore and understand warehouse and supply chain datasets.
- Profile datasets using Python and Pandas.
- Identify data-quality issues such as missing values and duplicates.
- Clean and standardize datasets.
- Integrate related business datasets.
- Validate data quality and consistency.
- Engineer analytical features.
- Develop business-focused KPIs and analytical insights.
- Analyse sales, purchasing, inventory, supplier, and customer performance.

---

## Project Structure

```text
CadetX-Warehouse-Analytic/

├── .vscode/
├── data/
│   ├── cleaned/
│   ├── integrated/
│   ├── features/
│   ├── kpis/
│   └── validation/
├── docs/
├── notebooks/
├── src/
├── week-01/
├── week-02/
├── week-03/
└── README.md
```

---

## Weekly Progress

### Week 01 — Data Foundation & Exploration

**Status: Completed ✅**

Week 01 focused on establishing the data foundation for the project.

#### Work Completed

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

#### Key Finding

`purchase_orders_header.csv` contains:

- **24,000 total rows**
- **2,370 missing `received_date` values**
- **0 duplicate rows**

The missing `received_date` values were retained as blank because they may represent purchase orders that have not yet been received. Artificial dates were not introduced to avoid changing the meaning of the source data.

#### Week 01 Documentation

Detailed Week 01 documentation is available in:

`week-01/README.md`

---

### Week 02 — Product & Inventory Analytics

**Status: Completed ✅**

Week 02 focused on product, inventory, and sales analysis.

#### Work Completed

- Analysed product performance and inventory data.
- Examined inventory health and stock movement.
- Analysed demand patterns and product-level sales performance.
- Developed analytical outputs for product and inventory insights.
- Prepared structured analytical results for further business analysis.

#### Key Analytical Areas

- Product performance
- Inventory health
- Stock movement
- Demand analysis
- Product-level sales analysis
- Inventory planning

---

### Week 03 — Data Analytics & KPI Foundation

**Status: Completed ✅**

Week 03 focused on transforming cleaned and integrated datasets into analytics-ready data and establishing the initial KPI foundation.

#### Work Completed

- Cleaned and prepared analytical datasets.
- Integrated product, inventory, and sales data.
- Created analytical features through feature engineering.
- Performed data validation and consistency checks.
- Created a structured data dictionary.
- Generated initial KPI outputs.
- Analysed demand patterns and product-level performance.

#### Week 03 Deliverables

| File | Purpose |
|---|---|
| `01_data_cleaning.py` | Data cleaning and preparation |
| `02_integration.py` | Product, inventory and sales data integration |
| `03_feature_engineering.py` | Analytical feature creation |
| `04_data_validation.py` | Data quality and consistency validation |
| `05_data_dictionary.md` | Dataset, field and relationship documentation |
| `06_first_kpis.py` | Initial KPI analysis |

#### Week 03 Outputs

The Week 03 workflow generated:

- Cleaned datasets
- Integrated datasets
- Feature-engineered dataset
- Data validation report
- Data validation summary
- KPI summary
- Top-demand product analysis
- Demand distribution analysis

#### Week 03 Analytical Focus

**Product Analytics**

- Product-level performance
- Demand movement
- Product KPI foundation

**Inventory Analytics**

- Current stock position
- Reorder-risk identification
- Overstock identification
- Inventory value analysis

**Sales Analytics**

- Quantity sold
- Sales value
- Average selling price
- Demand-level analysis

**Data Quality**

- Duplicate checks
- Missing-value checks
- Referential integrity
- Numeric validation
- Date validation
- Business-rule consistency

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
- Data Standardization
- Data Integration
- Data Quality Validation
- Missing Value Analysis
- Duplicate Detection
- Feature Engineering
- Exploratory Data Analysis
- KPI Development
- Dataset Relationship Analysis
- Business Analytics
- Documentation
- Version Control

---

## Project Roadmap

Future phases of the project will focus on:

- Developing advanced business KPIs.
- Analysing sales and purchase performance.
- Analysing inventory and stock levels.
- Evaluating supplier performance.
- Analysing customer purchasing behaviour.
- Creating analytical summaries and visualizations.
- Generating actionable business insights.
- Developing advanced analytical and predictive models.

---

## Repository

**GitHub Repository:**

https://github.com/kumari-arya05/CadetX-Warehouse-Analytic

---

## Author

**Kumari Arya**

**Program:** CadetX Virtual Work Experience Program

**Project:** Warehouse & Supply Chain Analytics

**Current Phase:** Week 03 — Data Analytics & KPI Foundation

---

## Project Status

| Phase | Status |
|---|---|
| Week 01 — Data Foundation & Exploration | ✅ Completed |
| Week 02 — Product & Inventory Analytics | ✅ Completed |
| Week 03 — Data Analytics & KPI Foundation | ✅ Completed |

**Current Project Status:** Week 03 Completed — Ready for the next sprint 🚀