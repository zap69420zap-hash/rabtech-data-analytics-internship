# KPI Dictionary — Task 05

| KPI | Definition | Calculation | Notes |
|---|---|---|---|
| Orders | Number of unique order IDs in selected records | Distinct count of order_id | Respects all active filters |
| Net Sales | Total net sales for selected records | Sum of net_sales | Displayed as ₹ |
| Average Order Value | Average net sales per selected row | Mean of net_sales | Dataset is one row per order after cleaning |
| Discount Amount | Total recorded discounts | Sum of discount_amount | Follows Task 03 cleaned values |
| Paid Orders % | Share of selected rows with payment status Paid | Paid rows / selected rows × 100 | Not the same as conversion rate |

## Dimensions
- Date: order_date, order_month
- Product: category
- Customer: customer_segment
- Geography: city
- Payment: payment_status

## Data quality and interpretation
- Source dataset is synthetic and intended for demonstrating analysis workflows.
- KPIs change dynamically with dashboard filters.
- These metrics are descriptive, not causal. Do not present them as actual company performance.
- If the data model changes to include multiple lines per order, calculate AOV at order level before dividing sales by order count.
