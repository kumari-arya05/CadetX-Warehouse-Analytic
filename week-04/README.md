# Week 04 — Warehouse Operations & Efficiency Analytics

## CadetX Virtual Work Experience

### Project Overview

Week 04 focused on **Warehouse Operations & Efficiency Analytics** as part of the CadetX Virtual Work Experience Program.

The objective of this sprint was to analyse warehouse capacity, utilisation, inventory movement, product distribution, warehouse performance, and operational bottlenecks using structured warehouse and inventory data.

The analysis was developed using Python and Pandas, with outputs generated as structured CSV datasets for further business analysis.

---

## Objectives

The main objectives of Week 04 were to:

* Analyse warehouse space utilisation
* Measure warehouse throughput and inventory movement
* Evaluate warehouse capacity usage
* Analyse product–warehouse alignment
* Develop warehouse performance scores
* Identify potential operational bottlenecks
* Benchmark warehouse utilisation and performance

---

## Data Sources

The analysis used the following project datasets:

* `branches.csv`
* `inventory_master.csv`
* `stock_ledger.csv`
* `sales_orders_header.csv`
* `sales_orders_lines.csv`

These datasets provide information about warehouse branches, inventory levels, stock movements, products, and sales orders.

---

## Analysis Workflow

The Week 04 workflow followed a structured analytical process:

**Data Preparation → Space Utilisation → Throughput → Capacity → Product–Warehouse Alignment → Performance Scoring → Bottleneck Detection → Utilisation Benchmarking**

---

## Key Analysis Areas

### 1. Warehouse Data Preparation

Prepared and validated warehouse-related datasets for downstream analysis.

Key activities included:

* Dataset loading
* Column standardisation
* Duplicate checks
* Missing-value checks
* Data-type validation
* Referential integrity checks
* Basic inventory and warehouse feature preparation

**Script:** `01_warehouse_data_preparation.py`

---

### 2. Warehouse Space Utilisation

Analysed warehouse capacity and current inventory levels to understand warehouse utilisation.

Key metrics included:

* Warehouse capacity
* Current stock
* Maximum stock
* Capacity utilisation percentage
* Available capacity
* Utilisation status

**Script:** `02_space_utilisation.py`

---

### 3. Warehouse Throughput Analysis

Analysed stock movements from the stock ledger to measure warehouse operational activity.

The analysis covered:

* Total movements
* Inbound quantity
* Outbound quantity
* Adjustment quantity
* Total throughput
* Unique products moved
* Outbound-to-inbound ratio
* Throughput ranking

**Script:** `03_warehouse_throughput.py`

---

### 4. Warehouse Capacity Analysis

Evaluated warehouse capacity usage and identified capacity pressure.

Key measures included:

* Remaining capacity
* Capacity utilisation gap
* Stock headroom
* Capacity status
* Capacity pressure
* Capacity risk level
* Capacity usage ranking

**Script:** `04_warehouse_capacity.py`

---

### 5. Product–Warehouse Alignment

Analysed how products are distributed across warehouses and branches.

The analysis included:

* Product–warehouse combinations
* Current stock allocation
* Number of warehouses holding each product
* Number of products handled by each warehouse
* Stock status
* Warehouse alignment classification

**Script:** `05_product_warehouse_alignment.py`

---

### 6. Warehouse Performance Scoring

Developed a warehouse performance score using multiple operational indicators.

The scoring framework incorporated:

* Capacity utilisation
* Warehouse throughput
* Product coverage

Warehouses were then classified into performance categories and ranked based on their calculated performance scores.

**Script:** `06_warehouse_performance.py`

---

### 7. Operational Bottleneck Detection

Identified potential warehouse bottlenecks using operational indicators.

The analysis considered:

* Capacity pressure
* High throughput
* Low performance
* Bottleneck indicator count
* Bottleneck status
* Bottleneck reasons
* Action priority

**Script:** `07_bottleneck_detection.py`

---

### 8. Warehouse Utilisation Benchmarking

Compared warehouses using utilisation, throughput, and performance metrics.

The benchmarking analysis included:

* Capacity utilisation
* Throughput
* Performance score
* Utilisation percentile
* Throughput percentile
* Performance percentile
* Overall benchmark score
* Benchmark category
* Benchmark ranking

**Script:** `08_utilisation_benchmarking.py`

---

## Project Outputs

The analysis generated structured CSV outputs covering:

* Warehouse Inventory Preparation
* Warehouse Space Utilisation
* Warehouse Throughput
* Warehouse Capacity
* Product–Warehouse Alignment
* Warehouse Performance
* Bottleneck Detection
* Warehouse Utilisation Benchmarking

The generated analytical outputs are stored in:

```text
data/features/
```

---

## Tools & Technologies

* Python
* Pandas
* CSV Data Analysis
* Git
* GitHub
* VS Code

---

## Skills Demonstrated

This sprint strengthened practical skills in:

* Data Preparation
* Data Validation
* Data Integration
* Warehouse Analytics
* Inventory Analytics
* Capacity Analysis
* Throughput Analysis
* Performance Scoring
* Bottleneck Detection
* Benchmarking
* Business-focused Data Analysis

---

## Project Structure

```text
week-04/
│
├── 01_warehouse_data_preparation.py
├── 02_space_utilisation.py
├── 03_warehouse_throughput.py
├── 04_warehouse_capacity.py
├── 05_product_warehouse_alignment.py
├── 06_warehouse_performance.py
├── 07_bottleneck_detection.py
├── 08_utilisation_benchmarking.py
└── README.md
```


