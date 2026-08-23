# Week 02 — Sprint Notes

## Sprint Goal

Complete Product & Inventory Analytics for the CadetX Heavy Supplier, Inventory & Warehouse Analytics project.

## Tasks Completed

1. Product Performance Analysis
2. Fast-Moving Product Identification
3. Slow-Moving & Dead Stock Identification
4. Inventory Turnover Analysis
5. Stock Health Assessment
6. Inventory Aging Analysis
7. ABC / Pareto Product Classification
8. Overstock & Understock Detection
9. Product Demand Trend Analysis

## Tools & Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- CSV datasets
- Visual Studio Code
- Git & GitHub

## Data Used

The analysis used:

- `products.csv`
- `inventory_master.csv`
- `sales_orders_lines.csv`
- `sales_orders_header.csv`

## Key Work Completed

### Product Analytics
Analysed product sales value and quantity sold to understand product performance and identify fast- and slow-moving products.

### Inventory Analytics
Analysed current stock, reorder levels, safety stock and maximum stock levels to assess inventory health and detect overstock and understock conditions.

### Inventory Turnover
Calculated product-level inventory turnover ratios using quantity sold and current stock.

### Inventory Aging
Used `last_purchase_date` as an aging proxy because the inventory dataset does not contain a stock-in date.

### ABC / Pareto Analysis
Classified products into A, B and C categories based on cumulative sales contribution.

### Demand Trend Analysis
Combined sales order lines with order dates to analyse monthly product demand trends.

## Deliverables

The sprint produced:

- Python analysis script
- Product performance results
- Fast-moving product results
- Slow-moving and dead-stock results
- Inventory turnover results
- Stock health results
- Inventory aging results
- ABC / Pareto classification results
- Overstock / understock results
- Product demand trend results
- Top demand product results
- Week-02 README documentation

## Challenges

The inventory dataset did not contain a direct stock-in date, so `last_purchase_date` was used as an aging proxy.

## Sprint Outcome

All nine Product & Inventory Analytics tasks were implemented successfully and the resulting analysis files were generated and uploaded to GitHub.

## Next Sprint

Continue with the next phase of analytics according to the CadetX roadmap and improve the project with additional analysis, visualisation and insights.