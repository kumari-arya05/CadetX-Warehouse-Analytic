# Week 06 — Product & Inventory Analytics

## CadetX Virtual Work Experience

This week focused on **Product & Inventory Analytics**, using sales and inventory data to identify product performance, inventory movement, stock health, inventory aging, and demand trends.

---

## Objectives

The main objectives of Week 06 were:

- Analyse product performance
- Identify fast-moving products
- Identify slow-moving and dead stock
- Measure inventory turnover
- Assess stock health
- Analyse inventory aging
- Perform ABC / Pareto classification
- Detect overstock and understock
- Analyse product demand trends

---

## Analyses Completed

### 1. Product Performance Analysis

Analysed product-level sales performance using:

- Total quantity sold
- Sales order lines
- Total sales value
- GST amount
- Average sales value
- Sales contribution percentage
- Performance ranking
- Performance category

**Script:** `01_product_performance.py`

**Output:** `product_performance.csv`

---

### 2. Fast-Moving Product Identification

Identified products with high sales movement based on quantity sold.

Key metrics included:

- Total quantity sold
- Sales order lines
- Average quantity per order
- Fast-moving ranking
- Movement category

**Script:** `02_fast_moving_products.py`

**Output:** `fast_moving_products.csv`

---

### 3. Slow-Moving & Dead Stock Identification

Identified products with low sales movement and potential dead stock.

Key metrics included:

- Total quantity sold
- Average quantity per order
- Slow-moving ranking
- Movement category
- Dead stock indicator
- Stock risk

**Script:** `03_slow_moving_dead_stock.py`

**Output:** `slow_moving_dead_stock.csv`

---

### 4. Inventory Turnover Analysis

Measured inventory movement using sales quantity and average inventory.

Key metrics included:

- Average inventory
- Total inventory
- Total quantity sold
- Inventory turnover ratio
- Turnover category
- Turnover ranking

**Script:** `04_inventory_turnover.py`

**Output:** `inventory_turnover.csv`

---

### 5. Stock Health Assessment

Assessed inventory health using current stock, reorder level, safety stock, and maximum stock.

Key metrics included:

- Current stock
- Reorder level
- Safety stock
- Maximum stock
- Stock utilisation percentage
- Stock health status
- Risk level
- Stock health score
- Risk ranking

**Script:** `05_stock_health_assessment.py`

**Output:** `stock_health_assessment.csv`

---

### 6. Inventory Aging Analysis

Analysed how long inventory remained without recent sales activity.

Key metrics included:

- Last sale date
- Days since last sale
- Aging category
- Aging risk
- Aging score
- Total quantity sold

**Script:** `06_inventory_aging.py`

**Output:** `inventory_aging.csv`

---

### 7. ABC / Pareto Product Classification

Classified products according to their contribution to total sales value.

The analysis included:

- Total sales value
- Sales contribution percentage
- Cumulative contribution percentage
- ABC category
- Sales ranking
- Pareto group

**Script:** `07_abc_pareto.py`

**Output:** `abc_pareto_products.csv`

---

### 8. Overstock & Understock Detection

Identified inventory above maximum levels or below reorder levels.

Key metrics included:

- Current stock
- Reorder level
- Safety stock
- Maximum stock
- Reorder gap
- Safety stock gap
- Overstock quantity
- Stock status
- Risk level
- Recommended action

**Script:** `08_overstock_understock.py`

**Output:** `overstock_understock.csv`

---

### 9. Product Demand Trend Analysis

Analysed product demand over time to identify increasing, stable, and decreasing demand patterns.

Key metrics included:

- Average monthly demand
- Total demand
- Peak monthly demand
- Demand months
- First month demand
- Last month demand
- Demand change percentage
- Demand trend
- Demand category
- Demand ranking

**Script:** `09_product_demand_trend.py`

**Output:** `product_demand_trend.csv`

---

## Project Structure

```text
week-06/
│
├── data/
│   ├── features/
│   │   ├── product_performance.csv
│   │   ├── fast_moving_products.csv
│   │   ├── slow_moving_dead_stock.csv
│   │   ├── inventory_turnover.csv
│   │   ├── stock_health_assessment.csv
│   │   ├── inventory_aging.csv
│   │   ├── abc_pareto_products.csv
│   │   ├── overstock_understock.csv
│   │   └── product_demand_trend.csv
│   │
│   └── raw/
│
├── scripts/
│   ├── 01_product_performance.py
│   ├── 02_fast_moving_products.py
│   ├── 03_slow_moving_dead_stock.py
│   ├── 04_inventory_turnover.py
│   ├── 05_stock_health_assessment.py
│   ├── 06_inventory_aging.py
│   ├── 07_abc_pareto.py
│   ├── 08_overstock_understock.py
│   └── 09_product_demand_trend.py
│
└── README.md
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- CSV
- VS Code
- Git
- GitHub

---

## Key Skills Developed

- Product-level data analysis
- Inventory analytics
- Feature engineering
- KPI development
- Sales performance analysis
- Inventory turnover analysis
- Stock risk assessment
- Inventory aging analysis
- ABC / Pareto analysis
- Demand trend analysis
- Business-oriented decision making
- Data-driven inventory management

---

## Outputs

All analysis scripts generate structured CSV outputs inside:

`week-06/data/features/`

These outputs can be used for further dashboard development, KPI reporting, and business insights.

---

## Conclusion

Week 06 strengthened practical skills in **Product & Inventory Analytics** by transforming transactional sales and inventory data into structured analytical outputs.

The completed analyses provide a foundation for understanding product performance, inventory efficiency, stock health, inventory risk, and changing product demand.