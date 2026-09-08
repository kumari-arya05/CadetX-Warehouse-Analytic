# Week 09 – Risk, Anomaly & Control Analytics

## Project
CadetX Warehouse Analytics – Heavy Supplier, Inventory & Warehouse Analytics

## Week 09 Objective

The objective of Week 09 is to identify inventory-related anomalies, potential stock shrinkage, operational risks, and data integrity issues using Python and the warehouse stock ledger dataset.

This analysis helps improve inventory control, detect unusual stock movements, monitor operational risks, and maintain data quality.

---

## Analyses Completed

### 1. Inventory Movement Anomaly Detection

**File:** `01_inventory_anomaly_detection.py`

This analysis identifies unusually high or low inventory movements using statistical threshold-based anomaly detection.

### Key Activities
- Loaded the stock ledger dataset
- Identified the inventory quantity field
- Calculated Q1, Q3 and IQR
- Created upper and lower anomaly thresholds
- Flagged unusual inventory movements
- Calculated anomaly scores
- Classified records as Normal or Anomaly

**Output:**

`outputs/inventory_movement_anomalies.csv`

---

### 2. Stock Shrinkage Detection

**File:** `02_stock_shrinkage_detection.py`

This analysis identifies potential stock shrinkage indicators from inventory records.

### Key Activities
- Checked for negative stock balances
- Identified unusually low stock levels
- Applied statistical threshold analysis
- Calculated shrinkage risk scores
- Classified shrinkage cases into Low, Medium and High risk
- Generated a stock shrinkage analysis report

**Output:**

`outputs/stock_shrinkage_analysis.csv`

---

### 3. Operational Risk Monitoring

**File:** `03_operational_risk_monitoring.py`

This analysis monitors inventory records for operational risk indicators.

### Key Activities
- Identified negative stock risk
- Detected unusual inventory movements
- Identified low or zero stock conditions
- Created operational risk classifications
- Generated risk reasons
- Calculated operational risk scores

**Output:**

`outputs/operational_risk_monitoring.csv`

---

### 4. Data Integrity & Error Detection

**File:** `04_data_integrity_check.py`

This analysis evaluates the quality and integrity of the stock ledger data.

### Key Activities
- Checked missing values
- Checked duplicate records
- Checked empty string values
- Checked negative numeric values
- Reviewed column data types
- Calculated unique values
- Created column-level data quality status
- Generated an overall data integrity status

**Outputs:**

`outputs/data_integrity_report.csv`

`outputs/data_integrity_summary.csv`

---

## Tools & Technologies

- Python
- Pandas
- NumPy
- CSV
- Statistical Analysis
- Data Quality Analysis
- Anomaly Detection
- Risk Classification

---

## Week 09 Output Files

| File | Description |
|---|---|
| `inventory_movement_anomalies.csv` | Inventory movement anomaly results |
| `stock_shrinkage_analysis.csv` | Potential stock shrinkage analysis |
| `operational_risk_monitoring.csv` | Operational risk monitoring results |
| `data_integrity_report.csv` | Column-level data quality report |
| `data_integrity_summary.csv` | Overall data integrity summary |

---

## Methodology

The Week 09 analysis follows these general steps:

1. Load the stock ledger dataset.
2. Inspect available columns and data types.
3. Identify inventory quantity information.
4. Perform statistical analysis for anomaly detection.
5. Detect potential stock shrinkage indicators.
6. Monitor operational inventory risks.
7. Perform data integrity and quality checks.
8. Export analysis results into CSV files.

---

## Key Business Benefits

The analysis supports warehouse and inventory management by helping to:

- Detect unusual inventory movements
- Identify potential stock shrinkage
- Monitor operational inventory risks
- Identify negative or low stock conditions
- Detect missing and duplicate records
- Improve data quality and reliability
- Support better inventory control decisions

---

## Conclusion

Week 09 extends the warehouse analytics project from predictive analysis into risk, anomaly, and control analytics.

The completed analyses provide a structured approach to identifying unusual inventory movements, potential stock shrinkage, operational risks, and data quality issues.

These outputs can support inventory control, warehouse monitoring, operational decision-making, and future Business Intelligence reporting.

---

## Status

**Week 09 – Completed**

### Completed Components

- [x] Inventory Movement Anomaly Detection
- [x] Stock Shrinkage Detection
- [x] Operational Risk Monitoring
- [x] Data Integrity & Error Detection
- [x] CSV Output Generation
- [x] Week 09 Documentation