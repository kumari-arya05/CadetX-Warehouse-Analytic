# CadetX Warehouse Analytics

## Week 1 – Data Foundation & Exploration

### Project Objective

Analyse the Heavy Supplier, Inventory & Warehouse dataset to understand the data structure and prepare it for further analytics.

### Week 1 Goals

- Explore all CSV datasets
- Understand rows and columns
- Identify data types
- Check missing values
- Check duplicate records
- Understand relationships between datasets
- Create initial data understanding

### Dataset Files

- branches.csv
- customers.csv
- inventory_master.csv
- invoices.csv
- payments.csv
- products.csv
- purchase_orders_header.csv
- purchase_orders_lines.csv
- sales_orders_header.csv
- sales_orders_lines.csv
- stock_ledger.csv
- suppliers.csv

### Week 1 Status

- Project structure created
- Dataset added to the `data` folder
- Week 1 folder created
- Data profiling completed for all CSV datasets
- Rows and columns inspected
- Data types inspected
- Missing values checked
- Duplicate records checked
- Initial dataset structure reviewed
- Data cleaning completed
- Cleaned datasets validated
- Date fields standardized
- Data quality validation completed
- Missing value analysis completed

### Data Profiling

Data profiling was performed using Python and Pandas.

The profiling script:

`notebooks/week01_data_profiling.py`

The following checks were performed:

- Dataset file discovery
- Row and column counts
- Column name inspection
- Data type inspection
- Missing value checks
- Duplicate row checks
- First five records review

### Data Cleaning

Data cleaning was performed using:

`src/data_cleaning.py`

The cleaning process included:

- Removing completely empty rows
- Removing duplicate rows
- Removing extra spaces from text fields
- Saving cleaned datasets separately
- Preserving the original datasets

Cleaned datasets are stored in:

`data/cleaned/`

### Data Type Standardization

Data type standardization was performed using:

`src/data_type_standardization.py`

The following date fields were checked and converted to datetime format where applicable:

- Customer purchase dates
- Invoice dates
- Due dates
- Payment dates
- Purchase order dates
- Expected delivery dates
- Received dates
- Other date-related fields

Invalid date values were checked during validation.

### Data Quality Validation

Data quality validation was performed using:

`src/data_quality_validation.py`

The following checks were completed:

- Missing value validation
- Duplicate row validation
- Date validation
- Dataset row and column validation

### Initial Findings

- All 12 CSV datasets were successfully processed.
- Cleaned datasets were successfully created in the `data/cleaned` folder.
- No duplicate rows were found during data quality validation.
- Most datasets contain no missing values.
- `purchase_orders_header.csv` contains 2,370 missing values in the `received_date` column.
- The missing `received_date` values were retained as blank because they may indicate orders that have not yet been received.
- Date fields were checked for invalid values.
- No invalid dates were identified in the validated date columns.

### Missing Value Analysis

Missing value analysis was performed using:

`src/handle_missing_values.py`

For `purchase_orders_header.csv`:

- Total rows: 24,000
- Missing `received_date` values: 2,370
- Duplicate rows: 0

The missing `received_date` values were not replaced with artificial dates because the absence of a received date may represent an order that has not yet been received.

### Week 1 Conclusion

Week 1 successfully established the data foundation for the CadetX Warehouse Analytics project.

The datasets were profiled, cleaned, standardized and validated. Initial data quality issues were identified and documented.

The cleaned datasets are now ready for further analysis and business KPI development.

### Next Steps

- Analyse relationships between datasets
- Identify primary and foreign key relationships
- Define business KPIs
- Analyse sales and purchase performance
- Analyse inventory and stock levels
- Analyse supplier performance
- Analyse customer purchasing behaviour
- Prepare data for business analytics and visualization