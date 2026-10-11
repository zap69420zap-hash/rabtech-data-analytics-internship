from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="RabTech Retail Analytics", page_icon="📊", layout="wide")
st.title("📊 Retail Performance Dashboard")
st.caption("RabTech Academy | Task 05 — Interactive KPI Visualizations | Synthetic practice dataset")

@st.cache_data
def load_data():
    candidates = [Path("../RabTech_Task03_Deliverables/clean_dataset.csv"), Path("RabTech_Task03_Deliverables/clean_dataset.csv"), Path("clean_dataset.csv")]
    for path in candidates:
        if path.exists():
            return pd.read_csv(path, parse_dates=["order_date"])
    st.error("Could not find clean_dataset.csv. Download it from Task 03 and place it next to app.py, or keep the Task 03 folder beside this folder.")
    st.stop()

df = load_data()
required = {"order_id","order_date","customer_segment","city","category","quantity","discount_pct","payment_status","gross_sales","discount_amount","net_sales","order_month"}
missing = required - set(df.columns)
if missing:
    st.error("Dataset is missing required columns: " + ", ".join(sorted(missing)))
    st.stop()

with st.sidebar:
    st.header("Filters")
    date_min, date_max = df["order_date"].min().date(), df["order_date"].max().date()
    dates = st.date_input("Order date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)
    categories = st.multiselect("Product category", sorted(df["category"].dropna().unique()), default=sorted(df["category"].dropna().unique()))
    cities = st.multiselect("City", sorted(df["city"].dropna().unique()), default=sorted(df["city"].dropna().unique()))
    segments = st.multiselect("Customer segment", sorted(df["customer_segment"].dropna().unique()), default=sorted(df["customer_segment"].dropna().unique()))
    statuses = st.multiselect("Payment status", sorted(df["payment_status"].dropna().unique()), default=sorted(df["payment_status"].dropna().unique()))

filtered = df.copy()
if isinstance(dates, (tuple, list)) and len(dates) == 2:
    filtered = filtered[filtered["order_date"].dt.date.between(dates[0], dates[1])]
filtered = filtered[filtered["category"].isin(categories) & filtered["city"].isin(cities) & filtered["customer_segment"].isin(segments) & filtered["payment_status"].isin(statuses)]

order_count = filtered["order_id"].nunique()
net_sales = filtered["net_sales"].sum()
avg_order_value = filtered["net_sales"].mean() if len(filtered) else 0
discount_total = filtered["discount_amount"].sum()
paid_share = (filtered["payment_status"].eq("Paid").mean() * 100) if len(filtered) else 0
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("Orders", f"{order_count:,}")
k2.metric("Net sales", f"₹{net_sales:,.0f}")
k3.metric("Average order value", f"₹{avg_order_value:,.0f}")
k4.metric("Discount amount", f"₹{discount_total:,.0f}")
k5.metric("Paid orders", f"{paid_share:.1f}%")
st.caption(f"Showing {len(filtered):,} of {len(df):,} rows. Sales figures are based on the selected filters.")

if filtered.empty:
    st.warning("No rows match these filters. Change one or more sidebar filters.")
    st.stop()

left, right = st.columns(2)
with left:
    by_category = filtered.groupby("category", as_index=False).agg(net_sales=("net_sales","sum"), orders=("order_id","nunique")).sort_values("net_sales", ascending=False)
    st.plotly_chart(px.bar(by_category, x="category", y="net_sales", color="category", title="Net Sales by Category", labels={"net_sales":"Net sales (₹)","category":"Category"}), use_container_width=True)
with right:
    monthly = filtered.groupby("order_month", as_index=False).agg(net_sales=("net_sales","sum"), orders=("order_id","nunique")).sort_values("order_month")
    st.plotly_chart(px.line(monthly, x="order_month", y="net_sales", markers=True, title="Monthly Net Sales Trend", labels={"order_month":"Month","net_sales":"Net sales (₹)"}), use_container_width=True)

left, right = st.columns(2)
with left:
    by_city = filtered.groupby("city", as_index=False).agg(net_sales=("net_sales","sum")).sort_values("net_sales", ascending=False)
    st.plotly_chart(px.bar(by_city, x="city", y="net_sales", title="Net Sales by City", labels={"city":"City","net_sales":"Net sales (₹)"}), use_container_width=True)
with right:
    status = filtered.groupby("payment_status", as_index=False).agg(orders=("order_id","nunique"), net_sales=("net_sales","sum"))
    st.plotly_chart(px.pie(status, names="payment_status", values="orders", hole=.45, title="Order Share by Payment Status"), use_container_width=True)

left, right = st.columns(2)
with left:
    st.plotly_chart(px.box(filtered, x="category", y="net_sales", color="category", title="Net Sales Distribution by Category", labels={"category":"Category","net_sales":"Net sales (₹)"}), use_container_width=True)
with right:
    st.plotly_chart(px.scatter(filtered, x="discount_pct", y="net_sales", color="category", hover_data=["city","customer_segment","payment_status"], title="Discount vs Net Sales", labels={"discount_pct":"Discount (%)","net_sales":"Net sales (₹)"}), use_container_width=True)

st.subheader("Filtered detail table")
st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)
st.download_button("Download filtered data (CSV)", data=filtered.to_csv(index=False).encode("utf-8"), file_name="rabtech_filtered_orders.csv", mime="text/csv")

with st.expander("KPI definitions"):
    st.markdown("""
    - **Orders:** distinct order IDs in the current selection.
    - **Net sales:** sum of net sales after discounts, as provided by the cleaned dataset.
    - **Average order value:** mean net sales per row/order in the selected data.
    - **Discount amount:** sum of recorded discount amounts.
    - **Paid orders:** percentage of selected rows whose payment status is Paid.
    
    **Important:** the source is synthetic practice data. These values are for demonstrating dashboard methods and are not real company results.
    """)
