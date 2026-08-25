# Week 03 — Data Dictionary

## Project

CadetX Virtual Work Experience — Heavy Supplier, Inventory & Warehouse Analytics

## Purpose

This data dictionary documents the main datasets, important fields,
data relationships, and analytical purpose used during Week 03.

---

## 1. Products Dataset

**Source:** `products.csv`

| Column | Description | Analytical Purpose |
|---|---|---|
| `product_id` | Unique identifier for a product | Product key |
| `product_name` | Name of the product | Product identification |
| `category` | Product category | Category analysis |
| `brand` | Product brand | Brand analysis |
| `unit_cost` | Cost per unit | Cost and margin analysis |
| `unit_price` | Selling price per unit | Revenue and margin analysis |

---

## 2. Inventory Dataset

**Source:** `inventory_master.csv`

| Column | Description | Analytical Purpose |
|---|---|---|
| `product_id` | Product identifier | Links inventory to products |
| `current_stock` | Current available stock | Inventory health analysis |
| `safety_stock` | Safety inventory level | Stock risk analysis |
| `reorder_level` | Replenishment trigger level | Reorder analysis |
| `max_stock` | Maximum target stock level | Overstock analysis |
| `last_purchase_date` | Most recent purchase date | Inventory aging analysis |

---

## 3. Sales Order Header Dataset

**Source:** `sales_orders_header.csv`

| Column | Description | Analytical Purpose |
|---|---|---|
| `so_id` | Sales order identifier | Order key |
| `customer_id` | Customer identifier | Customer analysis |
| `branch_id` | Branch identifier | Branch analysis |
| `order_date` | Order creation date | Demand and trend analysis |
| `delivery_date` | Delivery date | Delivery analysis |
| `order_status` | Order status | Order analysis |
| `payment_terms` | Payment terms | Payment analysis |
| `total_order_value` | Total order value | Revenue analysis |

---

## 4. Sales Order Lines Dataset

**Source:** `sales_orders_lines.csv`

| Column | Description | Analytical Purpose |
|---|---|---|
| `so_id` | Sales order identifier | Links lines to order header |
| `product_id` | Product identifier | Links sales to products |
| `quantity` | Quantity sold/ordered | Demand analysis |
| `unit_price` | Selling price per unit | Revenue analysis |
| `line_grand_total` | Total value of order line | Sales-value analysis |

---

## 5. Important Data Relationships

### Product and Inventory

```text
Products
   |
   | product_id
   |
Inventory