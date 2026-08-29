# Week 05 — Supplier & Procurement Analytics

## CadetX Virtual Work Experience

### Project Overview

Week 05 focused on **Supplier & Procurement Analytics** as part of the CadetX Virtual Work Experience Program.

The project analysed supplier contribution, supplier reliability, supplier performance, supplier dependency risk, critical suppliers, and supplier diversification using structured supplier and purchase order data.

The analysis was developed using **Python and Pandas**, with structured CSV outputs generated for further business analysis.

---

## Objectives

The main objectives of Week 05 were to:

- Analyse supplier contribution to overall purchasing
- Evaluate supplier reliability
- Compare supplier performance
- Identify supplier dependency risks
- Identify critical suppliers
- Analyse supplier diversification across product categories

---

## Data Sources

The analysis used the following cleaned project datasets:

- `suppliers.csv`
- `purchase_orders_header.csv`

These datasets provide information about suppliers, supplier characteristics, purchase orders, purchase values, delivery information, lead times, and reliability scores.

---

## Analysis Workflow

The Week 05 workflow followed a structured analytical process:

**Data Preparation → Supplier Contribution → Supplier Reliability → Supplier Performance → Dependency Risk → Critical Supplier Identification → Supplier Diversification**

---

## Key Analysis Areas

### 1. Supplier Contribution Analysis

Analysed supplier contribution to overall purchasing activity.

Key metrics included:

- Purchase order count
- Total purchase cost
- Total GST amount
- Total purchase value
- Contribution percentage
- Supplier contribution ranking
- Contribution category

**Script:** `01_supplier_contribution.py`

---

### 2. Supplier Reliability Analysis

Evaluated supplier reliability using supplier reliability scores and purchase order delivery information.

The analysis included:

- Purchase order count
- Total purchase value
- Expected delivery records
- Received delivery records
- Delivery completion rate
- Reliability score
- Reliability category
- Reliability ranking

**Script:** `02_supplier_reliability.py`

---

### 3. Supplier Performance Comparison

Compared suppliers using multiple performance indicators.

The performance analysis incorporated:

- Total purchase value
- Average purchase value
- Purchase order count
- Reliability score
- Lead time
- Purchase value score
- Lead time score
- Overall supplier performance score
- Performance category
- Performance ranking

**Script:** `03_supplier_performance.py`

---

### 4. Supplier Dependency Risk Analysis

Analysed supplier concentration based on their contribution to total purchase value.

Key measures included:

- Purchase order count
- Total purchase value
- Dependency percentage
- Dependency risk category
- Dependency risk score
- Dependency ranking

**Script:** `04_supplier_dependency_risk.py`

---

### 5. Critical Supplier Identification

Identified suppliers that may require greater operational attention using multiple indicators.

The analysis considered:

- Purchase contribution
- Lead time
- Reliability score
- High contribution indicator
- High lead time indicator
- Low reliability indicator
- Critical indicator count
- Critical supplier status
- Risk level
- Critical supplier ranking

**Script:** `05_critical_supplier_identification.py`

---

### 6. Supplier Diversification Analysis

Analysed supplier distribution across product categories and evaluated supplier concentration.

The analysis included:

- Supplier count by product category
- Region count
- Purchase value by supplier and category
- Category purchase share
- Supplier ranking within category
- Diversification risk
- Diversification status

**Script:** `06_supplier_diversification.py`

---

## Project Outputs

The analysis generated structured CSV outputs covering:

- Supplier Contribution
- Supplier Reliability
- Supplier Performance
- Supplier Dependency Risk
- Critical Supplier Identification
- Supplier Diversification

The generated analytical outputs are stored in:

```text
data/features/
```
### Generated Output Files

The generated analytical files are:

- `supplier_contribution.csv`
- `supplier_reliability.csv`
- `supplier_performance.csv`
- `supplier_dependency_risk.csv`
- `critical_supplier_identification.csv`
- `supplier_diversification.csv`

---

## Tools & Technologies

- **Python** — Data processing and analytical scripting
- **Pandas** — Data cleaning, transformation, aggregation, and analysis
- **NumPy** — Numerical calculations and analytical operations
- **CSV** — Structured data storage and analytical outputs
- **VS Code** — Development and analysis environment
- **Git & GitHub** — Version control and project management

---

## Analytical Features Created

The project transformed supplier and purchase order data into business-focused analytical features.

### Supplier Contribution Features

- Total purchase value
- Purchase contribution percentage
- Purchase order count
- Contribution ranking
- Contribution category

### Supplier Reliability Features

- Delivery completion rate
- Reliability score
- Reliability category
- Reliability ranking

### Supplier Performance Features

- Average purchase value
- Purchase value score
- Reliability score
- Lead time score
- Overall supplier performance score
- Performance category
- Performance ranking

### Supplier Risk Features

- Dependency percentage
- Dependency risk score
- Dependency risk category
- Dependency ranking
- Critical indicator count
- Critical supplier status
- Risk level

### Supplier Diversification Features

- Supplier count by category
- Region count
- Category purchase share
- Supplier ranking within category
- Diversification risk
- Diversification status

---

## Key Business Insights

The analysis provides insights into:

- Supplier contribution to overall procurement spend
- Supplier reliability and delivery performance
- Overall supplier performance across multiple KPIs
- Supplier dependency and concentration risk
- Critical suppliers requiring closer monitoring
- Supplier coverage across product categories
- Opportunities for improving supplier diversification

---

## Business Recommendations

Based on the analytical framework, procurement teams can:

- Monitor suppliers with high purchase contribution
- Reduce dependency on highly concentrated suppliers
- Develop backup suppliers for critical products
- Closely monitor suppliers with low reliability
- Review suppliers with high lead times
- Improve supplier diversification across product categories
- Use supplier performance scores for regular supplier evaluation
- Strengthen procurement risk management using data-driven indicators

---

## Project Structure

```text
Week-05-Supplier-Procurement-Analytics/
│
├── data/
│   ├── raw/
│   │   ├── suppliers.csv
│   │   └── purchase_orders_header.csv
│   │
│   └── features/
│       ├── supplier_contribution.csv
│       ├── supplier_reliability.csv
│       ├── supplier_performance.csv
│       ├── supplier_dependency_risk.csv
│       ├── critical_supplier_identification.csv
│       └── supplier_diversification.csv
│
├── scripts/
│   ├── 01_supplier_contribution.py
│   ├── 02_supplier_reliability.py
│   ├── 03_supplier_performance.py
│   ├── 04_supplier_dependency_risk.py
│   ├── 05_critical_supplier_identification.py
│   └── 06_supplier_diversification.py
│
└── README.md