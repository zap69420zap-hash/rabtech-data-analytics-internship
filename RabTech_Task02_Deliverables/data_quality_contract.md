# Retail Orders — Data Quality Contract

## Purpose and decision owner
This contract defines minimum quality requirements before retail-order KPIs or dashboards are published. **Proposed decision owner:** Sales Operations / Finance owner (confirm with mentor or business sponsor). **Data steward:** BI analyst. The supplied dictionary is the authority for field meanings and approved values.

## Dataset scope
- Source: `retail-orders-raw.csv` and `retail-data-dictionary.csv` supplied with the RabTech Task 02 brief.
- Observed sample size: 12 rows. This is a small training sample, not a production feed.
- Expected downstream use: order volume, sales value, discounts, payment outcomes and category mix.

## KPI publication rules
- Use the attached `KPI_Dictionary_and_Data_Quality_Contract.xlsx` for formulas, grain, filters, owner and cadence.
- Distinguish gross order value from net order value after discount.
- Do not label net order value as collected revenue unless settlement and refund treatment is explicitly applied.
- Use distinct `order_id` counts for order-level KPIs.

## Quality requirements
| Field | Required rule | Failure response |
|---|---|---|
| `order_id` | Required and unique after source review | Quarantine duplicates; compare source records and document canonical selection |
| `order_date` | Parseable date, ISO-normalized, on/after 2025-01-01 | Quarantine invalid dates; request source correction |
| `customer_segment` | Student, Fresher or Professional after normalization | Normalize known case variants; unknown values go to review |
| `city` | Required non-empty text | Do not invent a city; use Unknown only if approved and logged |
| `category` | Learning Kit, Course Access or Mentor Session | Quarantine unknown category pending owner review |
| `quantity` | Positive whole number | Reject/quarantine nonnumeric, zero, negative or fractional values |
| `unit_price` | Numeric INR amount >= 0 | Reject/quarantine invalid values; verify against price list |
| `discount_pct` | Numeric in [0, 100] | Review missing values; never silently impute zero without approval |
| `payment_status` | Paid, Pending, Failed or Refunded after normalization | Normalize case; quarantine unknown statuses |

## Thresholds and release gate
- Critical fields (`order_id`, `quantity`, `unit_price`): 100% valid.
- Allowed categories/statuses: 100% after approved normalization.
- Overall completeness target: at least 99% for a production feed, with 100% completeness for critical fields.
- No unresolved critical issues before publication. High-severity issues require documented owner sign-off.
- Freshness SLA must be agreed with the source owner; show the last refresh timestamp on any dashboard.

## Escalation and rollback
1. Stop KPI/dashboard refresh if a critical test fails.
2. Save the raw input and generated issue log for traceability.
3. Notify the data steward and decision owner with failing rule, affected rows, and business impact.
4. Correct upstream data or obtain explicit documented approval for a rule exception.
5. Re-run validation and compare KPI totals before releasing. Roll back to the last validated dataset if the new batch changes materially or fails the release gate.

## Observed issues in supplied sample
The sample includes an exact duplicate/order ID, inconsistent date format, an unparseable date (`2026-13-10`), missing city/date/discount, negative quantity, non-numeric quantity (`two`), discount above 100, and payment-status case inconsistency. The notebook logs these issues; it does not silently invent missing values.

## Limitations
The sample has only 12 rows. It is suitable for demonstrating KPI definitions and validation logic, not for making stable commercial claims. Confirm KPI definitions and the proposed owner roles before production use.
