# CadetX Warehouse Analytics

├── week-05/
├── week-06/
├── week-07/
# CadetX Warehouse Analytics

## Project Overview

**CadetX Warehouse Analytics** is a data analytics project developed as part of the **CadetX Virtual Work Experience Program**.

The project focuses on analysing Heavy Supplier, Inventory, Warehouse, Sales, Purchase, and Customer datasets to establish a reliable data foundation and generate meaningful business insights.

The project follows a structured analytics workflow:

**Data Profiling  Data Cleaning  Data Standardization  Data Integration  Data Validation  Feature Engineering  KPI Development**

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

 .vscode/
 data/
    cleaned/
    integrated/
    features/
    kpis/
    validation/
 docs/
 notebooks/
 src/
 week-01/
 week-02/
 week-03/
 week-04/
 README.md
```

---

## Weekly Progress

### Week 01  Data Foundation & Exploration

**Status: Completed **

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

### Week 02  Product & Inventory Analytics

**Status: Completed **

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

### Week 03  Data Analytics & KPI Foundation

**Status: Completed **

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

### Week 04  Warehouse Operations & Efficiency Analytics

**Status: Completed **

Week 04 focused on analysing warehouse capacity, utilisation, inventory movement, product distribution, warehouse performance, and operational bottlenecks.

#### Work Completed

- Prepared and validated warehouse-related datasets.
- Analysed warehouse space utilisation and capacity usage.
- Measured warehouse throughput and inventory movement.
- Analysed productwarehouse alignment.
- Developed warehouse performance scores.
- Identified potential operational bottlenecks.
- Benchmarked warehouse utilisation and performance.
- Generated structured CSV outputs for further business analysis.

#### Key Analytical Areas

- Warehouse Data Preparation
- Warehouse Space Utilisation
- Warehouse Throughput Analysis
- Warehouse Capacity Analysis
- ProductWarehouse Alignment
- Warehouse Performance Scoring
- Operational Bottleneck Detection
- Warehouse Utilisation Benchmarking

#### Week 04 Scripts

| Script | Analysis |
|---|---|
| `01_warehouse_data_preparation.py` | Warehouse data preparation and validation |
| `02_space_utilisation.py` | Warehouse space utilisation |
| `03_warehouse_throughput.py` | Warehouse throughput analysis |
| `04_warehouse_capacity.py` | Warehouse capacity analysis |
| `05_product_warehouse_alignment.py` | Productwarehouse alignment |
| `06_warehouse_performance.py` | Warehouse performance scoring |
| `07_bottleneck_detection.py` | Operational bottleneck detection |
| `08_utilisation_benchmarking.py` | Warehouse utilisation benchmarking |

#### Week 04 Outputs

The Week 04 analysis generated structured CSV outputs covering:

- Warehouse Inventory Preparation
- Warehouse Space Utilisation
- Warehouse Throughput
- Warehouse Capacity
- ProductWarehouse Alignment
- Warehouse Performance
- Bottleneck Detection
- Warehouse Utilisation Benchmarking

The generated analytical outputs are stored in:

```text
data/features/
```

#### Week 04 Documentation

Detailed Week 04 documentation is available in:

`week-04/README.md`

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
- Warehouse Analytics
- Inventory Analytics
- Capacity Analysis
- Throughput Analysis
- Performance Scoring
- Bottleneck Detection
- Benchmarking
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

**Current Phase:** Week 04  Warehouse Operations & Efficiency Analytics

---

## Project Status

| Phase | Status |
|---|---|
| Week 01  Data Foundation & Exploration |  Completed |
| Week 02  Product & Inventory Analytics |  Completed |
| Week 03  Data Analytics & KPI Foundation |  Completed |
| Week 04  Warehouse Operations & Efficiency Analytics |  Completed |

**Current Project Status:** Week 04 Completed  Ready for the next sprint 
---

### Week 05  Sales & Purchase Analytics

**Status: Completed ?**

Week 05 focused on sales, purchase, and business performance analytics.

#### Work Completed

- Analysed sales order performance.
- Analysed purchase order performance.
- Developed sales and purchase KPIs.
- Analysed revenue and order trends.
- Analysed supplier and procurement performance.
- Generated structured analytical outputs.

#### Week 05 Documentation

Detailed Week 05 documentation is available in:

week-05/README.md

---

### Week 06  Inventory & Warehouse Analytics

**Status: Completed ?**

Week 06 focused on inventory and warehouse analytics.

#### Work Completed

- Analysed inventory levels and stock movement.
- Analysed warehouse operations and efficiency.
- Developed inventory-related analytical features.
- Identified inventory risks and operational patterns.
- Generated structured analytical outputs.

#### Week 06 Documentation

Detailed Week 06 documentation is available in:

week-06/README.md

---

### Week 07  Supplier & Customer Analytics

**Status: Completed ?**

Week 07 focused on supplier performance, supplier risk, customer behaviour, and customer analytics.

#### Supplier Analytics

- Supplier Reliability Analysis
- Supplier Performance Comparison
- Supplier Dependency Risk Analysis
- Critical Supplier Identification

#### Customer Analytics

- Customer Purchase Behaviour Analysis
- RFM Analysis
- Customer Segmentation
- Customer Lifetime Value Analysis
- Customer Retention Analysis
- Customer Churn Analysis
- Customer Cohort Analysis
- High-Value Customer Identification
- At-Risk Customer Identification
- Customer Analytics Summary

#### Week 07 Documentation

Detailed Week 07 documentation is available in:

week-07/README.md

---

### Project Status

| Week | Status |
|------|--------|
| Week 01 | Completed |
| Week 02 | Completed |
| Week 03 | Completed |
| Week 04 | Completed |
| Week 05 | Completed |
| Week 06 | Completed |
| Week 07 | Completed |

