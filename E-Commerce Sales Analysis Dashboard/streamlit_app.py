"""
Streamlit Interactive Dashboard — E-Commerce Sales Analysis
Run: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="E-Commerce Sales Dashboard", layout="wide",
                   page_icon="🛒")

# ── Generate / Load Data ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 50000
    categories   = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books", "Beauty"]
    regions      = ["North", "South", "East", "West", "Central"]
    cat_prices   = {"Electronics":(5000,80000),"Clothing":(300,5000),
                    "Home & Kitchen":(500,20000),"Sports":(400,15000),
                    "Books":(150,1200),"Beauty":(200,3000)}
    cat_col      = np.random.choice(categories, n, p=[0.25,0.20,0.18,0.15,0.12,0.10])
    region_col   = np.random.choice(regions, n)
    price_col    = np.array([np.random.uniform(*cat_prices[c]) for c in cat_col]).round(2)
    qty_col      = np.random.randint(1, 6, n)
    discount_col = np.random.choice([0,5,10,15,20,25,30], n, p=[0.30,0.15,0.20,0.15,0.10,0.05,0.05])
    revenue_col  = (price_col * qty_col * (1 - discount_col/100)).round(2)
    cost_col     = (price_col * qty_col * np.random.uniform(0.45, 0.70, n)).round(2)
    profit_col   = (revenue_col - cost_col).round(2)
    dates        = pd.to_datetime(np.sort(np.random.choice(
                       pd.date_range("2023-01-01","2023-12-31",periods=n), n, replace=False)))
    df = pd.DataFrame({"order_date":dates,"category":cat_col,"region":region_col,
                       "quantity":qty_col,"unit_price":price_col,"discount_pct":discount_col,
                       "revenue":revenue_col,"cost":cost_col,"profit":profit_col,
                       "profit_margin":((profit_col/revenue_col)*100).round(2)})
    df["month"]      = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.strftime("%b")
    df["quarter"]    = df["order_date"].dt.quarter
    return df

df = load_data()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filters")
sel_region   = st.sidebar.multiselect("Region",   df["region"].unique(),   default=df["region"].unique())
sel_category = st.sidebar.multiselect("Category", df["category"].unique(), default=df["category"].unique())
sel_quarter  = st.sidebar.multiselect("Quarter",  [1,2,3,4], default=[1,2,3,4])

fdf = df[df["region"].isin(sel_region) &
         df["category"].isin(sel_category) &
         df["quarter"].isin(sel_quarter)]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🛒 E-Commerce Sales Analysis Dashboard")
st.caption("Janhavi Landge | Python • Pandas • Plotly • Streamlit | 50,000+ Records")
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("💰 Total Revenue",   f"₹{fdf['revenue'].sum()/1e7:.2f} Cr")
k2.metric("📈 Total Profit",    f"₹{fdf['profit'].sum()/1e7:.2f} Cr")
k3.metric("🛍️ Total Orders",   f"{len(fdf):,}")
k4.metric("🧾 Avg Order Value", f"₹{fdf['revenue'].mean():,.0f}")
k5.metric("📊 Profit Margin",   f"{(fdf['profit'].sum()/fdf['revenue'].sum()*100):.1f}%")

st.markdown("---")

# ── Row 1: Category + Monthly Trend ──────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    cat_rev = fdf.groupby("category")["revenue"].sum().reset_index().sort_values("revenue", ascending=True)
    fig = px.bar(cat_rev, x="revenue", y="category", orientation="h",
                 title="Revenue by Category", color="revenue",
                 color_continuous_scale="Blues", labels={"revenue":"Revenue (₹)"})
    fig.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    monthly = fdf.groupby(["month","month_name"])["revenue"].sum().reset_index().sort_values("month")
    fig = px.area(monthly, x="month_name", y="revenue",
                  title="Monthly Revenue Trend", color_discrete_sequence=["#2563EB"])
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Region Pie + Profit Margin ────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    reg = fdf.groupby("region")["revenue"].sum().reset_index()
    fig = px.pie(reg, values="revenue", names="region",
                 title="Revenue Share by Region", hole=0.4,
                 color_discrete_sequence=px.colors.sequential.Blues_r)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    cat_margin = fdf.groupby("category")["profit_margin"].mean().reset_index()
    fig = px.bar(cat_margin, x="category", y="profit_margin",
                 title="Avg Profit Margin by Category", color="profit_margin",
                 color_continuous_scale="RdYlGn", labels={"profit_margin":"Margin %"})
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3: Discount Impact ────────────────────────────────────────────────────
st.subheader("📉 Discount Impact on Profit Margin")
sample = fdf.sample(min(3000, len(fdf)), random_state=42)
fig = px.scatter(sample, x="discount_pct", y="profit_margin", color="category",
                 opacity=0.5, title="Discount % vs Profit Margin",
                 labels={"discount_pct":"Discount %","profit_margin":"Profit Margin %"})
fig.update_layout(height=380)
st.plotly_chart(fig, use_container_width=True)

# ── Insights ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("💡 Key Business Insights")
top_cat    = fdf.groupby("category")["revenue"].sum().idxmax()
top_region = fdf.groupby("region")["revenue"].sum().idxmax()
best_month = fdf.groupby("month_name")["revenue"].sum().idxmax()
low_margin = fdf.groupby("category")["profit_margin"].mean().idxmin()

col1, col2 = st.columns(2)
with col1:
    st.info(f"🏆 **{top_cat}** is the highest revenue category — prioritize promotions here.")
    st.info(f"📍 **{top_region}** region leads in sales — increase stock allocation.")
with col2:
    st.warning(f"📅 **{best_month}** is peak sales month — plan campaigns in advance.")
    st.warning(f"⚠️ **{low_margin}** has the lowest profit margin — review pricing/discounts.")
