# 🗄️ Advanced SQL Analytics Project


---

Demonstrate mastery of advanced SQL to extract business insights from a normalized relational retail database — covering revenue analysis, customer segmentation, product performance, and trend detection.

## 🗂️ Database Schema
```
customers ──┐
            ├──► orders ──► order_items ◄── products
            └──────────────────────────────┘
```
| Table | Rows | Key Columns |
|---|---|---|
| customers | 200 | customer_id, city, segment, join_date |
| products | 45 | product_id, category, sub_category, unit_price |
| orders | 5,000 | order_id, customer_id, order_date, ship_mode |
| order_items | 12,000+ | item_id, order_id, product_id, quantity, revenue, profit |

## 📊 Queries Written (9 Advanced Queries)

| # | Query | SQL Concepts Used |
|---|---|---|
| Q1 | Overall KPIs | Aggregation, JOINs |
| Q2 | Revenue by Category | GROUP BY, ORDER BY |
| Q3 | Top 10 Customers | Multi-table JOINs |
| Q4 | Monthly Trend | strftime, GROUP BY |
| Q5 | Running Revenue Total | **Window Function** (SUM OVER, Moving Avg) |
| Q6 | Customer Segmentation | **CTE**, NTILE, CASE WHEN |
| Q7 | Underperforming Products | **Subquery** in HAVING |
| Q8 | City-wise Performance | Multi-level aggregation |
| Q9 | Product Ranking in Category | **RANK() PARTITION BY** |

## 💡 Key Insights
1. Electronics drives highest revenue but furniture has better margins
2. Top 25% customers (High Value tier) contribute ~60% of revenue
3. High-discount products (>20%) consistently show below-average margins
4. Month-over-month running totals reveal clear Q4 revenue spikes

## 🚀 How to Run
```bash
pip install pandas numpy
python sql_project.py
```
> No external database needed — SQLite runs in-memory!

## 🛠️ SQL Skills Demonstrated
- **Joins:** INNER JOIN across 4 tables
- **Aggregations:** SUM, AVG, COUNT, GROUP BY, HAVING
- **CTEs:** Multi-step logic with WITH clause
- **Window Functions:** SUM OVER, AVG OVER, RANK, NTILE, PARTITION BY
- **Subqueries:** Correlated subquery in HAVING clause
- **Date Functions:** strftime for month/year extraction
- **Conditional Logic:** CASE WHEN for customer tier labeling

