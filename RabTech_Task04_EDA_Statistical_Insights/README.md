# RabTech Academy — Task 04
## EDA & Statistical Insights

### Files
- `task04_eda_statistical_insights.ipynb` — descriptive statistics, category/city/segment/monthly summaries, correlations, charts, box plots, three hypothesis tests, and top-five findings.
- The notebook exports `category_summary.csv`, `city_summary.csv`, `segment_summary.csv`, `monthly_trends.csv`, `correlation_matrix.csv`, `hypothesis_tests.csv`, and `top_5_findings.csv` when all cells are run.

### Run
1. Open the notebook in Jupyter or Google Colab.
2. Keep the Task 03 folder in the same repository. The notebook reads `../RabTech_Task03_Deliverables/clean_dataset.csv`. If you download the notebook separately, place `clean_dataset.csv` in the same folder as the notebook.
3. Run all cells from top to bottom.
4. Confirm the CSV reports were created.

### Hypothesis tests
- H1: Paid vs non-Paid mean net sales — Welch independent-samples t-test.
- H2: Discount percentage vs net sales — Pearson correlation.
- H3: Mean net sales across categories — one-way ANOVA.
- Significance level: 0.05.

### Transparency
The Task 03 dataset is synthetic practice data, not real company/customer data. Results demonstrate EDA methods only. Statistical association does not establish causation.
