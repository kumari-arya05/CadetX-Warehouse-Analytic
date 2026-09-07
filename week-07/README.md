# Week 07 – Supplier, Customer & Predictive Analytics

## Project Overview

Week 07 focuses on supplier performance analysis and customer analytics for the Warehouse Analytics project.

The analysis uses supplier, purchase order, customer, and sales order data to identify supplier risks, understand customer purchasing behaviour, evaluate customer value, and identify retention and churn risks.

---

## Objectives

- Analyse supplier reliability and delivery performance
- Compare supplier performance
- Identify supplier dependency and procurement risks
- Identify critical suppliers
- Analyse customer purchase behaviour
- Perform RFM analysis
- Segment customers
- Estimate Customer Lifetime Value (CLV)
- Analyse customer retention
- Analyse customer churn
- Perform customer cohort analysis
- Identify high-value customers
- Identify at-risk customers
- Create an overall customer analytics summary

---

## Dataset Used

The Week 07 analysis uses the following datasets:

- `suppliers.csv`
- `purchase_orders_header.csv`
- `purchase_orders_lines.csv`
- `customers.csv`
- `sales_orders_header.csv`
- `sales_orders_lines.csv`

---

## Supplier Analytics

### 1. Supplier Reliability Analysis

Evaluates supplier delivery performance using:

- Actual delivery days
- Expected delivery days
- Delivery delay
- On-time delivery
- On-time delivery rate
- Reliability rating

Output:

`outputs/supplier_reliability_analysis.csv`

### 2. Supplier Performance Comparison

Compares suppliers using:

- Total orders
- On-time orders
- Average delivery days
- Average delay days
- Total purchase cost
- Average order value
- On-time delivery rate
- Performance rating

Output:

`outputs/supplier_performance_comparison.csv`

### 3. Supplier Dependency Risk Analysis

Measures supplier dependency using:

- Order dependency percentage
- Purchase value dependency percentage
- Dependency risk score
- Dependency risk classification
- Critical supplier flag

Output:

`outputs/supplier_dependency_risk.csv`

### 4. Critical Supplier Identification

Identifies suppliers that require additional attention based on:

- High purchase value dependency
- Low supplier reliability

Outputs:

- `outputs/critical_supplier_identification.csv`
- `outputs/critical_supplier_summary.csv`

---

## Customer Analytics

### 5. Customer Purchase Behaviour

Analyses customers using:

- Total orders
- Total order value
- Average order value
- First purchase date
- Last purchase date
- Customer activity
- Purchase behaviour classification

Outputs:

- `outputs/customer_purchase_behaviour.csv`
- `outputs/customer_purchase_behaviour_summary.csv`

### 6. RFM Analysis

RFM analysis evaluates customers using:

- Recency
- Frequency
- Monetary value
- RFM score
- Customer segment

Outputs:

- `outputs/rfm_analysis.csv`
- `outputs/rfm_segment_summary.csv`

### 7. Customer Segmentation

Customers are grouped into meaningful segments based on RFM scores.

Output:

`outputs/customer_segmentation.csv`

Summary:

`outputs/customer_segment_summary.csv`

### 8. Customer Lifetime Value

Estimates customer value using:

- Total revenue
- Customer lifetime
- Annual customer value
- Estimated 3-year CLV
- CLV segment

Outputs:

- `outputs/customer_lifetime_value.csv`
- `outputs/customer_lifetime_value_summary.csv`

### 9. Customer Retention Analysis

Identifies retained and one-time customers using customer order history.

Outputs:

- `outputs/customer_retention_analysis.csv`
- `outputs/customer_retention_summary.csv`

### 10. Customer Churn Analysis

Classifies customers based on the number of days since their last purchase.

Output:

`outputs/customer_churn_analysis.csv`

Summary:

`outputs/customer_churn_summary.csv`

### 11. Customer Cohort Analysis

Analyses customer retention across purchase cohorts using:

- Cohort month
- Cohort index
- Active customers
- Cohort size
- Retention rate
- Revenue

Outputs:

- `outputs/customer_cohort_analysis.csv`
- `outputs/customer_cohort_retention_matrix.csv`

### 12. High-Value Customer Identification

Identifies high-value customers based on estimated 3-year CLV.

Outputs:

- `outputs/high_value_customer_identification.csv`
- `outputs/high_value_customer_summary.csv`

### 13. At-Risk Customer Identification

Identifies customers requiring retention attention based on purchase recency.

Outputs:

- `outputs/at_risk_customer_identification.csv`
- `outputs/at_risk_customer_summary.csv`

### 14. Customer Analytics Summary

Combines major customer analytics metrics into one summary.

Output:

`outputs/customer_analytics_summary.csv`

---

## Project Structure

```text
week-07/
│
├── data/
│   ├── suppliers.csv
│   ├── purchase_orders_header.csv
│   ├── purchase_orders_lines.csv
│   ├── customers.csv
│   ├── sales_orders_header.csv
│   └── sales_orders_lines.csv
│
├── scripts/
│   ├── supplier_reliability_analysis.py
│   ├── 02_supplier_performance_comparison.py
│   ├── 03_supplier_dependency_risk.py
│   ├── 04_critical_supplier_identification.py
│   ├── 05_customer_purchase_behaviour.py
│   ├── 06_rfm_analysis.py
│   ├── 07_customer_segmentation.py
│   ├── 08_customer_lifetime_value.py
│   ├── 09_customer_retention_analysis.py
│   ├── 10_customer_churn_analysis.py
│   ├── 11_customer_cohort_analysis.py
│   ├── 12_high_value_customer_identification.py
│   ├── 13_at_risk_customer_identification.py
│   └── 14_customer_analytics_summary.py
│
├── outputs/
│   └── CSV analysis results
│
└── README.md