# 📦 E-Commerce Data Engineering Pipeline (Synthetic Dataset)

This project is a complete end-to-end data engineering pipeline built using Cursor IDE with GitHub Copilot assistance. It includes synthetic e-commerce data generation, ingestion into SQLite, and advanced multi-table SQL analytics.

The goal is to create a clean, unique, and production-like system demonstrating real-world data engineering workflows.


## 🚀 Project Highlights

### 1️⃣ AI-Assisted Synthetic Data Generation
- Generates 5 realistic e-commerce datasets:
  - `customers.csv`, `products.csv`, `orders.csv`, `order_items.csv`, `reviews.csv`
- Configurable size (`--scale`) and reproducible via `--seed`
- Fully realistic numeric, categorical, and date fields
- Enables experimentation without real data

### 2️⃣ Robust SQLite Ingestion
- Automatically creates tables with **primary and foreign keys**
- Loads all CSV datasets into `database/ecommerce.db`
- Simulates a professional **ETL workflow**
- Supports integrity checks and error handling

### 3️⃣ Advanced Multi-Table SQL Analytics
- Queries combine multiple tables (`JOIN`, `LEFT JOIN`) for insights
- Aggregate functions (`SUM()`, `AVG()`, `COUNT()`) and nested subqueries
- Example insights:
  - Top 5 Customers by Lifetime Spend
  - Top 5 Products by Revenue and Units Sold
  - Monthly Revenue for the Last 5 Months
  - Top 5 Customers by Average Review Rating
  - Product Revenue Contribution by Category

 ## 📁 Project Structure
 ecommerce-analytics-pipeline/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── prompts/                           # AI prompts used
│   ├── 01_data_generation.md
│   ├── 02_database_design.md
│   └── 03_analytics_queries.md
├── data/                              # Generated datasets
│   ├── products.csv
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── reviews.csv
├── scripts/                           # Python automation
│   ├── generate_data.py
│   ├── setup_database.py
│   ├── run_queries.py
│   └── utils.py
├── database/                          # SQLite database
│   └── ecommerce.db
├── queries/                           # SQL queries
│   ├── schema.sql
│   └── analytics.sql
├── results/                           # Query outputs
│   └── insights.txt
└── docs/                              # Additional documentation
    └── data_dictionary.md
                     
