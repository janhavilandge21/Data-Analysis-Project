"""
E-Commerce Sales Analysis & Dashboard
======================================
Author  : Janhavi Landge
Tools   : Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit
Dataset : Synthetic 50,000+ record e-commerce sales data
Goal    : Identify revenue trends, top products, regional performance & KPIs
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─── 1. DATA GENERATION (Simulates real 50K record dataset) ───────────────────

np.random.seed(42)
n = 50000

categories   = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books", "Beauty"]
regions      = ["North", "South", "East", "West", "Central"]
payment_mode = ["Credit Card", "UPI", "Net Banking", "COD", "Debit Card"]

cat_prices = {
    "Electronics": (5000, 80000),
    "Clothing":    (300,  5000),
    "Home & Kitchen": (500, 20000),
    "Sports":      (400,  15000),
    "Books":       (150,  1200),
    "Beauty":      (200,  3000),
}

cat_col      = np.random.choice(categories, n, p=[0.25,0.20,0.18,0.15,0.12,0.10])
region_col   = np.random.choice(regions, n)
payment_col  = np.random.choice(payment_mode, n, p=[0.30,0.28,0.15,0.17,0.10])
qty_col      = np.random.randint(1, 6, n)

price_col = np.array([
    np.random.uniform(*cat_prices[c]) for c in cat_col
]).round(2)

discount_col   = np.random.choice([0, 5, 10, 15, 20, 25, 30], n,
                                   p=[0.30,0.15,0.20,0.15,0.10,0.05,0.05])
revenue_col    = (price_col * qty_col * (1 - discount_col / 100)).round(2)
cost_col       = (price_col * qty_col * np.random.uniform(0.45, 0.70, n)).round(2)
profit_col     = (revenue_col - cost_col).round(2)
profit_margin  = ((profit_col / revenue_col) * 100).round(2)

dates = pd.date_range("2023-01-01", "2023-12-31", periods=n)
dates = pd.to_datetime(np.sort(np.random.choice(dates, n, replace=False)))

# Introduce realistic nulls (2%)
return_flag = np.random.choice([0, 1], n, p=[0.93, 0.07])

df = pd.DataFrame({
    "order_id":      range(1, n+1),
    "order_date":    dates,
    "category":      cat_col,
    "region":        region_col,
    "payment_mode":  payment_col,
    "quantity":      qty_col,
    "unit_price":    price_col,
    "discount_pct":  discount_col,
    "revenue":       revenue_col,
    "cost":          cost_col,
    "profit":        profit_col,
    "profit_margin": profit_margin,
    "returned":      return_flag,
})

# Inject nulls for realism
null_idx = np.random.choice(df.index, int(n*0.02), replace=False)
df.loc[null_idx[:int(n*0.01)], "discount_pct"] = np.nan
df.loc[null_idx[int(n*0.01):], "payment_mode"] = np.nan

print("=" * 55)
print("       E-COMMERCE SALES ANALYSIS — JANHAVI LANDGE")
print("=" * 55)

# ─── 2. DATA CLEANING ─────────────────────────────────────────────────────────

print(f"\n[1] Raw Data Shape       : {df.shape}")
print(f"    Null Values          :\n{df.isnull().sum()[df.isnull().sum()>0]}")

df["discount_pct"].fillna(df["discount_pct"].median(), inplace=True)
df["payment_mode"].fillna(df["payment_mode"].mode()[0], inplace=True)

df["month"]      = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%b")
df["quarter"]    = df["order_date"].dt.quarter
df["week"]       = df["order_date"].dt.isocalendar().week.astype(int)

print(f"\n[2] After Cleaning Shape : {df.shape}")
print(f"    Remaining Nulls      : {df.isnull().sum().sum()}")
print(f"    Date Range           : {df['order_date'].min().date()} → {df['order_date'].max().date()}")

# ─── 3. KPI CALCULATIONS ──────────────────────────────────────────────────────

total_revenue   = df["revenue"].sum()
total_profit    = df["profit"].sum()
total_orders    = df["order_id"].nunique()
avg_order_value = df["revenue"].mean()
overall_margin  = (total_profit / total_revenue * 100)
return_rate     = df["returned"].mean() * 100

print(f"\n{'─'*55}")
print("  KEY PERFORMANCE INDICATORS (KPIs)")
print(f"{'─'*55}")
print(f"  Total Revenue       : ₹{total_revenue:>14,.0f}")
print(f"  Total Profit        : ₹{total_profit:>14,.0f}")
print(f"  Total Orders        :  {total_orders:>14,}")
print(f"  Avg Order Value     : ₹{avg_order_value:>14,.2f}")
print(f"  Overall Profit Mrg  :  {overall_margin:>13.2f}%")
print(f"  Return Rate         :  {return_rate:>13.2f}%")
print(f"{'─'*55}")

# ─── 4. CATEGORY ANALYSIS ─────────────────────────────────────────────────────

cat_summary = df.groupby("category").agg(
    Total_Revenue = ("revenue", "sum"),
    Total_Profit  = ("profit",  "sum"),
    Orders        = ("order_id","count"),
    Avg_Margin    = ("profit_margin","mean"),
).sort_values("Total_Revenue", ascending=False).round(2)
cat_summary["Revenue_Share_%"] = (cat_summary["Total_Revenue"] / total_revenue * 100).round(2)

print(f"\n[3] CATEGORY PERFORMANCE:\n")
print(cat_summary.to_string())

# ─── 5. REGIONAL ANALYSIS ─────────────────────────────────────────────────────

region_summary = df.groupby("region").agg(
    Revenue = ("revenue","sum"),
    Profit  = ("profit","sum"),
    Orders  = ("order_id","count"),
).sort_values("Revenue", ascending=False).round(2)

print(f"\n[4] REGIONAL PERFORMANCE:\n")
print(region_summary.to_string())

# ─── 6. MONTHLY TREND ─────────────────────────────────────────────────────────

monthly = df.groupby(["month","month_name"]).agg(
    Revenue = ("revenue","sum"),
    Profit  = ("profit","sum"),
    Orders  = ("order_id","count"),
).reset_index().sort_values("month")

print(f"\n[5] MONTHLY REVENUE TREND (Top 3 months):")
print(monthly.nlargest(3,"Revenue")[["month_name","Revenue","Profit","Orders"]].to_string(index=False))

# ─── 7. INSIGHTS ──────────────────────────────────────────────────────────────

top_cat    = cat_summary.index[0]
top_cat_pct= cat_summary.iloc[0]["Revenue_Share_%"]
top_region = region_summary.index[0]
best_month = monthly.loc[monthly["Revenue"].idxmax(), "month_name"]
low_margin_cat = cat_summary["Avg_Margin"].idxmin()

print(f"\n{'─'*55}")
print("  BUSINESS INSIGHTS")
print(f"{'─'*55}")
print(f"  1. '{top_cat}' drives {top_cat_pct:.1f}% of total revenue —")
print(f"     focus promotions here for maximum ROI.")
print(f"  2. '{top_region}' region is the top revenue contributor —")
print(f"     consider increasing inventory allocation.")
print(f"  3. '{best_month}' is the peak sales month —")
print(f"     plan flash sales & campaigns around it.")
print(f"  4. '{low_margin_cat}' has the lowest avg margin —")
print(f"     review pricing strategy or reduce discounts.")
print(f"  5. Return rate is {return_rate:.2f}% — investigate top returned")
print(f"     categories to reduce operational loss.")
print(f"{'─'*55}")

# ─── 8. VISUALIZATIONS ────────────────────────────────────────────────────────

sns.set_theme(style="whitegrid", palette="Blues_r")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("E-Commerce Sales Analysis Dashboard — Janhavi Landge",
             fontsize=16, fontweight="bold", y=1.01)

# Plot 1: Revenue by Category
cat_plot = cat_summary.reset_index()
sns.barplot(data=cat_plot, x="Total_Revenue", y="category",
            palette="Blues_r", ax=axes[0,0])
axes[0,0].set_title("Revenue by Category", fontweight="bold")
axes[0,0].set_xlabel("Revenue (₹)")
axes[0,0].set_ylabel("")

# Plot 2: Monthly Revenue Trend
axes[0,1].plot(monthly["month_name"], monthly["Revenue"]/1e6,
               marker="o", color="#1B3A6B", linewidth=2.5)
axes[0,1].fill_between(monthly["month_name"], monthly["Revenue"]/1e6,
                        alpha=0.15, color="#1B3A6B")
axes[0,1].set_title("Monthly Revenue Trend (₹ Millions)", fontweight="bold")
axes[0,1].tick_params(axis='x', rotation=45)

# Plot 3: Region-wise Profit
region_plot = region_summary.reset_index()
sns.barplot(data=region_plot, x="region", y="Profit",
            palette="viridis", ax=axes[0,2])
axes[0,2].set_title("Profit by Region", fontweight="bold")
axes[0,2].set_xlabel("")
axes[0,2].set_ylabel("Profit (₹)")

# Plot 4: Profit Margin by Category
sns.barplot(data=cat_plot, x="category", y="Avg_Margin",
            palette="coolwarm", ax=axes[1,0])
axes[1,0].set_title("Avg Profit Margin % by Category", fontweight="bold")
axes[1,0].tick_params(axis='x', rotation=20)
axes[1,0].set_ylabel("Margin (%)")

# Plot 5: Revenue Share Pie
axes[1,1].pie(cat_plot["Revenue_Share_%"], labels=cat_plot["category"],
              autopct="%1.1f%%", startangle=90,
              colors=sns.color_palette("Blues_r", len(cat_plot)))
axes[1,1].set_title("Revenue Share by Category", fontweight="bold")

# Plot 6: Discount vs Profit Margin scatter (sample)
sample = df.sample(1000, random_state=42)
axes[1,2].scatter(sample["discount_pct"], sample["profit_margin"],
                  alpha=0.4, color="#2563EB", s=20)
axes[1,2].set_title("Discount % vs Profit Margin", fontweight="bold")
axes[1,2].set_xlabel("Discount %")
axes[1,2].set_ylabel("Profit Margin %")

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=150, bbox_inches="tight")
print("\n[✓] Dashboard saved → sales_dashboard.png")
print("[✓] Analysis complete! Run streamlit_app.py for interactive dashboard.")

# Save cleaned data for Streamlit
df.to_csv("cleaned_sales_data.csv", index=False)
print("[✓] Cleaned data saved → cleaned_sales_data.csv")
