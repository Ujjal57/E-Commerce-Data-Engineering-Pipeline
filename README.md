# 📦 E-Commerce Data Engineering Pipeline (Synthetic Dataset)


![Python](https://img.shields.io/badge/Python-3.11-blue)
![SQLite](https://img.shields.io/badge/SQLite-database-orange)
![License](https://img.shields.io/badge/License-MIT-green)

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
├── prompts.md                  # Consolidated AI prompts used for data generation, ingestion, and SQL queries
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
## 📝 AI Prompts

This project was built using **Cursor IDE** and **GitHub Copilot**. All AI prompts used for generating data, creating the database ingestion scripts, and writing multi-table SQL analytics queries are consolidated into a single file:

- `prompts.md` – Contains all prompts, including:
  - Generating synthetic e-commerce datasets
  - Creating the SQLite ingestion scripts
  - Writing multi-table SQL analytics queries

## 🤝 Tools & Technologies

- **Cursor IDE** – AI-assisted coding environment for generating scripts and queries  
- **Python 3.11** – Core programming language  
  - **Pandas** – Data manipulation and CSV handling  
  - **NumPy** – Numeric operations for synthetic data generation  
- **SQLite3** – Lightweight relational database for ingestion and queries  
- **SQL** – Multi-table queries, joins, aggregations, subqueries  
- **CSV** – Input and output file format for datasets  
- **Git & GitHub** – Version control and repository management  

## 📈 Outputs

The pipeline generates multiple useful business insights from the synthetic e-commerce dataset. Example outputs include:

### 1️⃣ Top 5 Customers by Lifetime Spend
| customer_id | name             | orders_count | lifetime_spend |
|------------|-----------------|-------------|----------------|
| 142        | David Robinson   | 12          | 3,327.82       |
| 29         | Jacob Hunter     | 12          | 2,167.17       |
| 486        | Morgan Glass     | 8           | 1,932.34       |
| 497        | Nicholas James   | 6           | 1,721.43       |
| 272        | Thomas Williams  | 8           | 1,539.75       |

### 2️⃣ Top 5 Products by Revenue and Units Sold
| product_id | name           | category  | revenue   | units_sold |
|------------|----------------|----------|----------|------------|
| 21         | Each Finish    | Home     | 9,641.84 | 52         |
| 152        | Air Fill       | Sports   | 8,936.56 | 68         |
| 101        | However Turn   | Sports   | 8,593.44 | 48         |
| 177        | Point Notice   | Beauty   | 5,565.00 | 60         |
| 132        | Heavy Of       | Clothing | 5,002.89 | 57         |

### 3️⃣ Monthly Revenue Trends (Last 5 Months)
| month    | total_revenue |
|---------|---------------|
| 2025-11 | 4,231.71      |
| 2025-10 | 8,511.22      |
| 2025-09 | 11,583.39     |
| 2025-08 | 11,021.09     |
| 2025-07 | 12,196.76     |

### 4️⃣ Top 5 Customers by Average Review Rating
| customer_id | name            | review_count | avg_rating |
|------------|----------------|--------------|------------|
| 426        | James Rodriguez | 5            | 4.80       |
| 428        | Thomas Cohen    | 4            | 4.75       |
| 40         | William Lynch   | 3            | 4.67       |
| 55         | Nicholas Edwards| 3            | 4.67       |
| 161        | Kiara Smith     | 3            | 4.67       |

### 5️⃣ Revenue Contribution by Product Category
| category     | revenue       | pct_of_revenue |
|-------------|---------------|----------------|
| Electronics | 64,903.04     | 0.2484         |
| Clothing    | 44,342.38     | 0.1697         |
| Sports      | 41,824.41     | 0.1600         |
| Home        | 38,873.78     | 0.1488         |
| Beauty      | 26,384.59     | 0.1010         |
| Books       | 23,229.86     | 0.0889         |
| Toys        | 21,772.17     | 0.0833         |

> These outputs are **generated dynamically** from the synthetic datasets using `queries.sql` on the SQLite database.

## 📝 License

© 2025 Ujjal Kumar Dey. **All rights reserved.**

No part of this project may be used, copied, or modified without my explicit permission.
