-- ==========================================================
-- 📊 E-Commerce Data Engineering Pipeline (Synthetic Dataset)
-- ==========================================================
-- This file contains multiple SQL queries for analytics on
-- the synthetic e-commerce database created by ingest_to_sqlite.py.
--
-- Usage:
--   Run all queries in SQLite using:
--     sqlite3 database/ecommerce.db ".read queries.sql"
--
-- Each section below explores different business insights.
-- ==========================================================


-- ==========================================================
-- 1️⃣ Top 10 Customers by Lifetime Spend
-- ----------------------------------------------------------
-- Shows customers with the highest total spending across
-- all completed orders.
-- ==========================================================
SELECT
    c.customer_id,
    c.name,
    COUNT(DISTINCT o.order_id) AS orders_count,
    ROUND(COALESCE(SUM(o.total), 0), 2) AS lifetime_spend
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
ORDER BY lifetime_spend DESC
LIMIT 10;


-- ==========================================================
-- 2️⃣ Top 10 Products by Revenue and Units Sold
-- ----------------------------------------------------------
-- Identifies products that generate the highest sales and
-- total quantity sold, based on completed orders.
-- ==========================================================
SELECT
    p.product_id,
    p.name,
    p.category,
    SUM(oi.line_total) AS revenue,
    SUM(oi.quantity) AS units_sold
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
GROUP BY p.product_id, p.name, p.category
ORDER BY revenue DESC
LIMIT 10;


-- ==========================================================
-- 3️⃣ Monthly Revenue for the Last 12 Months
-- ----------------------------------------------------------
-- Calculates total revenue per month (YYYY-MM format) for
-- completed orders in the last year.
-- ==========================================================
WITH months AS (
    SELECT
        strftime('%Y-%m', order_date) AS month,
        SUM(total) AS revenue
    FROM orders
    WHERE status = 'completed' AND order_date IS NOT NULL
    GROUP BY month
)
SELECT
    month,
    ROUND(revenue, 2) AS total_revenue
FROM months
ORDER BY month DESC
LIMIT 12;


-- ==========================================================
-- 4️⃣ Top 20 Customers by Average Review Rating
-- ----------------------------------------------------------
-- Finds customers who provided the highest average ratings.
-- Filters to include only customers with at least 3 reviews.
-- ==========================================================
SELECT
    c.customer_id,
    c.name,
    COUNT(r.review_id) AS review_count,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM customers c
JOIN reviews r ON r.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
HAVING review_count >= 3
ORDER BY avg_rating DESC, review_count DESC
LIMIT 20;


-- ==========================================================
-- 5️⃣ Product Revenue Contribution by Category
-- ----------------------------------------------------------
-- Breaks down total sales revenue by product category and
-- shows each category's contribution as a percentage.
-- ==========================================================
SELECT
    p.category,
    SUM(oi.line_total) AS revenue,
    ROUND(
        SUM(oi.line_total) * 1.0 /
        (SELECT SUM(oi2.line_total)
         FROM order_items oi2
         JOIN orders o2 ON o2.order_id = oi2.order_id
         WHERE o2.status = 'completed'),
    4) AS pct_of_revenue
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;


-- ==========================================================
-- ✅ End of File — queries.sql
-- ==========================================================
