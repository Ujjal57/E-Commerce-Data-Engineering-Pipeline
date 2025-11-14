# 📦 E-Commerce Data Engineering Pipeline (Synthetic Dataset)

This project is a complete end-to-end data engineering pipeline built using Cursor IDE with GitHub Copilot assistance. It includes synthetic e-commerce data generation, ingestion into SQLite, and advanced multi-table SQL analytics.

The goal is to create a clean, unique, and production-like system demonstrating real-world data engineering workflows.



What I built
- `generate_data.py`: configurable synthetic data generator (customers, products, orders, order_items, reviews). Uses `Faker`, `numpy`, and `pandas`.
-- `ingest_to_sqlite.py`: creates `ecommerce.db` at the project root (outside `data/`), tables with foreign keys and indexes, and bulk inserts from CSV.
- `queries.sql`: set of join queries and aggregations demonstrating multi-table joins and useful analytics.
- `run_windows.bat`: convenience helper for Windows (install deps, generate, ingest).
- `requirements.txt`: Python dependencies.

How this is advanced & unique
- Realistic distributions: price uses log-normal for realistic skew, quantity and statuses follow tailored probabilities.
- Consistency: order totals are computed from order_items to ensure referential correctness.
- Configurable scale and seed for reproducible experiments.
- Indexes and FK constraints added for realistic DB behavior and performant joins.

Quickstart (Windows)
1. Create a virtual environment (recommended):

    python -m venv .venv
    .venv\Scripts\activate

2. Install dependencies:

    python -m pip install -r requirements.txt

3. Run the pipeline (generate + ingest):

    python src\generate_data.py --seed 42 --scale 1
    python src\ingest_to_sqlite.py

Note: The script will NOT write `data/customer_ltv.csv` by default. To generate
the `customer_ltv.csv` file include the `--ltv` flag when running the ingest step:

    python src\ingest_to_sqlite.py --ltv

4. Run queries (example using `sqlite3`):

    sqlite3 ecommerce.db ".read queries.sql"

Cursor IDE Prompts (tailored and advanced)

1) Prompt to generate synthetic ecom data (use this in Cursor IDE to generate code or to ask the assistant to produce data files):

"You are a data engineer. Write a Python script that generates realistic synthetic e-commerce data with five CSV files: customers, products, orders, order_items, and reviews. Requirements: use Faker for names and addresses, use realistic distributions (log-normal for prices, skewed quantity distributions), compute order totals from order_items, include timestamps over the last 2-3 years, accept CLI args `--seed` and `--scale` for reproducibility and scalability, and write CSVs into a `data/` folder. Keep the schema simple but consistent with foreign keys. Include comments and usage examples." 

2) Prompt to ingest the code/data into a SQLite database (sqlite):

"You are a backend engineer. Write a Python script that reads five CSV files (customers.csv, products.csv, orders.csv, order_items.csv, reviews.csv) from a `data/` folder, creates a SQLite DB `ecommerce.db` at the project root (outside `data/`), defines normalized tables with appropriate types and foreign keys, bulk inserts rows efficiently, and creates indexes that improve join/query performance. Ensure the script is idempotent and prints the DB path on completion. Provide CLI usage." 

3) Prompt to generate a SQL query that joins multiple tables and generates an output:

"You are a SQL expert. Given tables customers, products, orders, order_items, and reviews in SQLite, write SQL queries that show: (a) top 10 customers by lifetime spend (only completed orders), (b) top 10 products by revenue and units sold, (c) monthly revenue for the last 12 months, and (d) customers with highest average review rating (min 3 reviews). Use efficient aggregation and explain any indexes that help performance." 

4) Advanced Cursor prompt to make your submission unique (ask assistant to enhance):

"Enhance the existing pipeline: add realistic seasonality to orders (higher in Nov-Dec), simulate discounts and coupon codes that affect item prices (store coupon code and discount percent), include a small set of product variants (color/size) for a subset of products, and produce a final CSV `customer_ltv.csv` that contains customer_id, lifetime_spend, orders_count, average_order_value, and last_order_date. Provide code and explanation." 

GitHub push instructions

1. Initialize Git and commit:

    git init
    git add .
    git commit -m "Add synthetic ecom generator, ingest script, and queries"

2. Create a new GitHub repo (use GitHub UI) and then push:

    git remote add origin https://github.com/<your-username>/<repo>.git
    git branch -M main
    git push -u origin main

What I can do next for you
- Run the scripts here locally and show sample outputs (I can't run code on your machine unless you ask me to run commands).
- Add the advanced features from Prompt #4 (seasonality, coupons, variants) to make your submission stand out — I can implement them now.
