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
 
## ✨ Features

- **End-to-End Data Pipeline:** Complete workflow from synthetic data generation to database ingestion and multi-table SQL analytics.  
- **Realistic Synthetic Datasets:** Generates 5 e-commerce CSV files (`customers`, `products`, `orders`, `order_items`, `reviews`) suitable for experimentation and learning.  
- **Advanced SQL Analytics:** Supports multi-table joins, aggregations (`SUM`, `AVG`, `COUNT`), subqueries, and generates meaningful business insights.  
- **Robust Data Ingestion:** Ensures referential integrity, proper data types, error handling, and data validation when loading into SQLite.  
- **Configurable & Reproducible:** Dataset size can be scaled, and results are reproducible using a seed parameter.  

 ## 📁 Project Structure
 ```
E-Commerce-Data-Engineering-Pipeline/
├── database/                   # SQLite database after ingestion
├── src/
│   ├── generate_data.py        # Script to generate synthetic CSV data
│   └── ingest_to_sqlite.py     # Script to ingest CSVs into SQLite
├── prompts.md                  # Generated synthetic CSV datasets
├── queries.sql                 # Combined Markdown file with all prompts
├── queries.sql                 # Advanced multi-table SQL analytics queries
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🛠 Installation & Usage

1. **Clone the repository from GitHub:**

```bash
git clone https://github.com/Ujjal57/E-Commerce-Data-Engineering-Pipeline.git
cd E-Commerce-Data-Engineering-Pipeline
```
2. **Install dependencies:**

```bash
pip install -r requirements.txt
```
3. **Generate synthetic data:**

```bash
python src/generate_data.py --seed 42 --scale 1
```
4. **Build the SQLite database:**

```bash
python src/ingest_to_sqlite.py
```
5. **Run analytics queries:**
```
```bash
sqlite3 database/ecommerce.db ".read queries.sql"
```
