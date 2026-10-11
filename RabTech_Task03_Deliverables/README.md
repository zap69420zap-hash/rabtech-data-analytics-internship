# RabTech Academy — Task 03
## Data Ingestion, Cleaning & Preprocessing with Pandas

### Deliverables
- `retail-orders-raw-12000.csv`: synthetic raw dataset (12,000+ rows).
- `task03_data_cleaning_preprocessing.ipynb`: Pandas profiling, cleaning, validation and feature engineering.
- `clean_dataset.csv`: cleaned output dataset.

### Run
Keep the CSV and notebook in the same folder. Open the notebook in Jupyter or Google Colab and run all cells.

### Cleaning rules
- Parse dates; invalid dates become missing and those rows are excluded.
- Convert quantity, unit price and discount to numeric values.
- Standardize category text casing and whitespace.
- Remove exact duplicate rows.
- Exclude records with missing required fields, invalid dates, non-positive quantity/price, or discount outside 0–100.
- Missing discount is filled with 0 as a project assumption; confirm with a data owner before production use.
- Create gross_sales, discount_amount, net_sales and order_month.

### Transparency
This is a synthetic practice dataset, not real company/customer data. It is used to demonstrate a 10,000+ row cleaning workflow.
