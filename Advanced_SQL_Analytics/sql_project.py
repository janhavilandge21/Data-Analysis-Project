"""
Advanced SQL Analytics Project
================================
Author : Janhavi Landge
Tools  : Python, SQLite, Pandas, SQL (Joins, CTEs, Window Functions, Subqueries)
Goal   : Demonstrate advanced SQL skills on a retail sales database
"""

import sqlite3
import pandas as pd
import numpy as np

print("=" * 60)
print("   ADVANCED SQL ANALYTICS PROJECT — JANHAVI LANDGE")
print("=" * 60)

# ─── 1. DATABASE SETUP ────────────────────────────────────────────────────────
conn = sqlite3.connect(":memory:")
cur  = conn.cursor()

cur.executescript("""
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    customer_name TEXT,
    city          TEXT,
    segment       TEXT,
    join_date     DATE
);
CREATE TABLE products (
    product_id    INTEGER PRIMARY KEY,
    product_name  TEXT,
    category      TEXT,
    sub_category  TEXT,
    unit_price    REAL
);
CREATE TABLE orders (
    order_id      INTEGER PRIMARY KEY,
    customer_id   INTEGER,
    order_date    DATE,
    ship_mode     TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
CREATE TABLE order_items (
    item_id       INTEGER PRIMARY KEY,
    order_id      INTEGER,
    product_id    INTEGER,
    quantity      INTEGER,
    discount      REAL,
    revenue       REAL,
    profit        REAL,
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

# ── Seed data ──
np.random.seed(42)
cities    = ["Mumbai","Delhi","Bangalore","Hyderabad","Chennai","Pune","Kolkata","Ahmedabad"]
segments  = ["Consumer","Corporate","Home Office"]
cats      = {"Electronics":["Phones","Tablets","Accessories"],
             "Furniture":["Chairs","Tables","Bookcases"],
             "Office Supplies":["Pens","Paper","Binders"]}
ship_modes= ["Standard","Second Class","First Class","Same Day"]

customers = [(i+1, f"Customer_{i+1}", np.random.choice(cities),
              np.random.choice(segments),
              f"202{np.random.randint(0,4)}-{np.random.randint(1,13):02d}-01")
             for i in range(200)]
cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)

products, pid = [], 1
for cat, subs in cats.items():
    for sub in subs:
        for j in range(5):
            price = np.random.uniform(200, 50000)
            products.append((pid, f"{sub}_Product_{j+1}", cat, sub, round(price,2)))
            pid += 1
cur.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)

order_id, item_id = 1, 1
orders_data, items_data = [], []
for _ in range(5000):
    cid  = np.random.randint(1, 201)
    yr   = np.random.randint(2021, 2024)
    mo   = np.random.randint(1, 13)
    day  = np.random.randint(1, 28)
    odate= f"{yr}-{mo:02d}-{day:02d}"
    ship = np.random.choice(ship_modes, p=[0.6,0.2,0.15,0.05])
    orders_data.append((order_id, cid, odate, ship))

    for _ in range(np.random.randint(1, 4)):
        prod   = np.random.randint(1, pid)
        qty    = np.random.randint(1, 6)
        disc   = np.random.choice([0,0.05,0.1,0.15,0.2,0.3], p=[0.35,0.15,0.2,0.15,0.1,0.05])
        uprice = products[prod-1][4]
        rev    = round(uprice * qty * (1 - disc), 2)
        prof   = round(rev * np.random.uniform(0.1, 0.45), 2)
        items_data.append((item_id, order_id, prod, qty, disc, rev, prof))
        item_id += 1
    order_id += 1

cur.executemany("INSERT INTO orders VALUES (?,?,?,?)", orders_data)
cur.executemany("INSERT INTO order_items VALUES (?,?,?,?,?,?,?)", items_data)
conn.commit()
print("\n[✓] Database created with 4 tables: customers, products, orders, order_items")

# ─── 2. QUERIES ───────────────────────────────────────────────────────────────

def run(title, sql, n=10):
    df = pd.read_sql_query(sql, conn)
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print(f"{'─'*60}")
    print(df.head(n).to_string(index=False))
    return df

# Q1: Basic aggregation — KPIs
run("Q1: OVERALL KPIs", """
SELECT
    COUNT(DISTINCT o.order_id)           AS total_orders,
    COUNT(DISTINCT o.customer_id)        AS unique_customers,
    ROUND(SUM(oi.revenue), 2)            AS total_revenue,
    ROUND(SUM(oi.profit),  2)            AS total_profit,
    ROUND(AVG(oi.revenue), 2)            AS avg_order_item_value,
    ROUND(SUM(oi.profit)/SUM(oi.revenue)*100, 2) AS profit_margin_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
""")

# Q2: Revenue by category
run("Q2: REVENUE & PROFIT BY CATEGORY", """
SELECT
    p.category,
    COUNT(DISTINCT oi.item_id)            AS items_sold,
    ROUND(SUM(oi.revenue), 2)             AS total_revenue,
    ROUND(SUM(oi.profit),  2)             AS total_profit,
    ROUND(SUM(oi.profit)/SUM(oi.revenue)*100, 2) AS profit_margin_pct
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC
""")

# Q3: Top 10 customers by revenue
run("Q3: TOP 10 CUSTOMERS BY REVENUE", """
SELECT
    c.customer_name,
    c.city,
    c.segment,
    COUNT(DISTINCT o.order_id)   AS total_orders,
    ROUND(SUM(oi.revenue), 2)    AS total_revenue,
    ROUND(SUM(oi.profit),  2)    AS total_profit
FROM customers c
JOIN orders o      ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id  = oi.order_id
GROUP BY c.customer_id
ORDER BY total_revenue DESC
LIMIT 10
""")

# Q4: Monthly revenue trend using strftime
run("Q4: MONTHLY REVENUE TREND", """
SELECT
    strftime('%Y', o.order_date)       AS year,
    strftime('%m', o.order_date)       AS month,
    COUNT(DISTINCT o.order_id)         AS orders,
    ROUND(SUM(oi.revenue), 2)          AS monthly_revenue,
    ROUND(SUM(oi.profit),  2)          AS monthly_profit
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY year, month
ORDER BY year, month
""")

# Q5: Window function — Running total revenue
run("Q5: RUNNING TOTAL REVENUE (Window Function)", """
WITH monthly AS (
    SELECT
        strftime('%Y-%m', o.order_date)   AS month,
        ROUND(SUM(oi.revenue), 2)          AS monthly_rev
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY month
)
SELECT
    month,
    monthly_rev,
    ROUND(SUM(monthly_rev) OVER (ORDER BY month), 2)          AS running_total,
    ROUND(AVG(monthly_rev) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m
FROM monthly
ORDER BY month
""")

# Q6: CTE — Customer segmentation by RFM-style value
run("Q6: CUSTOMER VALUE SEGMENTATION (CTE)", """
WITH customer_stats AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.segment,
        COUNT(DISTINCT o.order_id)   AS frequency,
        ROUND(SUM(oi.revenue), 2)    AS monetary,
        MAX(o.order_date)            AS last_order_date
    FROM customers c
    JOIN orders o       ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id    = oi.order_id
    GROUP BY c.customer_id
),
ranked AS (
    SELECT *,
        NTILE(4) OVER (ORDER BY monetary DESC)  AS value_quartile
    FROM customer_stats
)
SELECT
    CASE value_quartile
        WHEN 1 THEN 'High Value'
        WHEN 2 THEN 'Medium-High'
        WHEN 3 THEN 'Medium-Low'
        WHEN 4 THEN 'Low Value'
    END                          AS customer_tier,
    COUNT(*)                     AS customer_count,
    ROUND(AVG(monetary), 2)      AS avg_revenue,
    ROUND(AVG(frequency), 1)     AS avg_orders
FROM ranked
GROUP BY value_quartile
ORDER BY value_quartile
""")

# Q7: Products with below-average profit margin
run("Q7: UNDERPERFORMING PRODUCTS (Subquery)", """
SELECT
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(SUM(oi.revenue), 2)                       AS total_revenue,
    ROUND(SUM(oi.profit)/SUM(oi.revenue)*100, 2)    AS margin_pct
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id
HAVING margin_pct < (
    SELECT AVG(profit/revenue)*100 FROM order_items WHERE revenue > 0
)
ORDER BY margin_pct ASC
LIMIT 10
""")

# Q8: City-wise performance
run("Q8: CITY-WISE REVENUE PERFORMANCE", """
SELECT
    c.city,
    COUNT(DISTINCT c.customer_id)        AS customers,
    COUNT(DISTINCT o.order_id)           AS orders,
    ROUND(SUM(oi.revenue), 2)            AS total_revenue,
    ROUND(SUM(oi.revenue)/COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
GROUP BY c.city
ORDER BY total_revenue DESC
""")

# Q9: Rank products within each category
run("Q9: PRODUCT RANKING WITHIN CATEGORY (RANK Window)", """
WITH cat_product AS (
    SELECT
        p.category,
        p.product_name,
        ROUND(SUM(oi.revenue), 2) AS revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category, p.product_id
)
SELECT
    category,
    product_name,
    revenue,
    RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rank_in_category
FROM cat_product
QUALIFY rank_in_category <= 3
ORDER BY category, rank_in_category
""", n=15)

conn.close()
print(f"\n{'─'*60}")
print("  ✅ All 9 SQL queries executed successfully!")
print("  Skills shown: JOINs, GROUP BY, CTEs, Window Functions,")
print("  Subqueries, CASE WHEN, NTILE, RANK, PARTITION BY")
print(f"{'─'*60}")
