# RabTech Task 02 — KPI Dictionary & Data Quality Contract

## Deliverables
- `KPI_Dictionary_and_Data_Quality_Contract.xlsx` — KPI definitions plus field-level quality contract.
- `task02_data_quality_profile.ipynb` — executable profiling, validation, issue logging and baseline KPIs.
- `data_quality_contract.md` — readable contract with thresholds, escalation and release gate.
- `retail-orders-raw.csv`, `retail-data-dictionary.csv` — original supplied inputs.

## Run the notebook
Keep both CSVs in the same folder as the notebook. Install `pandas` and `numpy`, then open the notebook in Jupyter or Google Colab and run all cells. It exports `task02_column_profile.csv`, `task02_issue_log.csv`, and `task02_kpi_baseline.csv`.

## Important limitations
The provided raw dataset contains only 12 rows. The deliverable explicitly describes sample-level results and does not claim to meet the 10,000+ row requirement of Task 03. Missing discount is flagged for business approval instead of silently being set to zero. Duplicate order IDs are flagged for source review.
