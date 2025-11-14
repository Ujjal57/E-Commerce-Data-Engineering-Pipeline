# 📝 Cursor IDE AI Prompts for E-Commerce Data Engineering Pipeline

This file documents the AI prompts used in **Cursor IDE** to create the synthetic e-commerce data pipeline project.  

Each prompt corresponds to a specific task: generating data, ingesting it into SQLite, and creating multi-table SQL analytics queries.

---

## 1️⃣ Cursor IDE Prompt: Generate Synthetic Data

```text
# Task:
# Generate realistic synthetic e-commerce datasets in Python.

# Requirements:
# - Create 5 CSV files: customers.csv, products.csv, orders.csv, order_items.csv, reviews.csv
# - Each CSV must have proper columns and realistic relationships.
# - Numeric and date fields must be valid and consistent.
# - Totals in orders must match sum of line items.
# - Allow a --seed parameter for reproducibility.
# - Allow a --scale parameter to control dataset size.

# CSV Structure:
# customers.csv: customer_id, name, email, phone
# products.csv: product_id, name, category, price
# orders.csv: order_id, customer_id, order_date, total, status
# order_items.csv: order_item_id, order_id, product_id, quantity, line_total
# reviews.csv: review_id, customer_id, product_id, rating, review_text, review_date

# Output:
# - Python script: generate_data.py
# - Writes 5 CSV files under data/ folder
```

## 2️⃣ Cursor IDE Prompt: Ingest Data into SQLite

```text 
# Task:
# Write a Python script to ingest synthetic CSV datasets into a SQLite database.

# Requirements:
# - Read 5 CSV files: customers.csv, products.csv, orders.csv, order_items.csv, reviews.csv
# - Create a SQLite database: ecommerce.db inside database/ folder
# - Create tables with proper PRIMARY KEY and FOREIGN KEY constraints
# - Load CSV data into corresponding tables
# - Maintain referential integrity and correct data types
# - Include error handling for missing or invalid data
# - Ensure workflow mimics a professional ETL process

# Output:
# - Python script: ingest_to_sqlite.py
# - Database created under database/ecommerce.db
```

3️⃣ Cursor IDE Prompt: Multi-Table SQL Queries

```text
# Task:
# Write SQL queries for advanced analytics on the e-commerce SQLite database.

# Requirements:
# - Include joins, aggregations, subqueries, and proper ordering
# - Perform analytics on multiple tables simultaneously
# - Save all queries in a single file: queries.sql

# Analytics Queries:
# 1. Top 10 customers by lifetime spend (sum of completed orders)
# 2. Top 10 products by revenue and units sold
# 3. Monthly revenue trends for the last 12 months
# 4. Top 20 customers by average review rating (minimum 3 reviews)
# 5. Revenue contribution by product category
# 6. Customer lifetime value (spending, order count, average order, last order date)

# Output:
# - SQL file: queries.sql
# - Ready to execute in SQLite using:
#   sqlite3 database/ecommerce.db ".read queries.sql"
