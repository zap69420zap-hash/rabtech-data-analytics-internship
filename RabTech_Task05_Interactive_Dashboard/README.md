# Task 05 — Interactive Dashboard & KPI Visualizations

## Deliverables
- app.py — interactive Streamlit dashboard with KPI cards, filters, six charts, detail table, and CSV download.
- requirements.txt — Python dependencies.
- KPI_DICTIONARY.md — metric definitions and calculation rules.

## Dashboard features
- KPI cards: order count, net sales, average order value, total discounts, paid-order share.
- Monthly net sales trend.
- Net sales by category and city.
- Payment-status order share.
- Category net-sales box plot.
- Discount-versus-net-sales scatter plot.
- Interactive sidebar filters and downloadable filtered records.

## Run locally
1. Download this repository or keep the Task 03 and Task 05 folders together.
2. Install Python 3.10+.
3. Install dependencies: pip install -r requirements.txt
4. Run: streamlit run app.py from this folder.
5. Ensure the Task 03 clean_dataset.csv is in the sibling RabTech_Task03_Deliverables folder, or put a copy beside app.py.

## Google Colab option
Upload app.py, requirements.txt, and Task 03 clean_dataset.csv to a Colab session, install the requirements, and launch Streamlit using your preferred approved tunnel. Do not publish sensitive information or API tokens.

## Data transparency
This dashboard uses the synthetic dataset prepared in Task 03. It does not represent real RabTech customer or sales data. Net sales values reflect the dataset's documented preprocessing assumptions.
