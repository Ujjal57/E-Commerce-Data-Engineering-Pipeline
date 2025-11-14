"""
E-commerce Data Ingestion Script

Loads synthetic e-commerce CSV files from `synthetic_ecom_data/` into a
normalized SQLite database located at `database/ecommerce.db`.

Usage:
    python src/ingest_to_sqlite.py
    python src/ingest_to_sqlite.py --ltv
    python src/ingest_to_sqlite.py --db-path database/ecommerce.db --replace
"""

import argparse
import csv
import os
import sqlite3
from typing import Dict, Iterable, List


# SQL TABLE SCHEMA        

SQL_CREATE: Dict[str, str] = {
    "customers": """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            address TEXT,
            join_date TEXT
        );
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            sku TEXT
        );
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            total REAL,
            status TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        );
    """,
    "order_items": """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            line_total REAL,
            FOREIGN KEY(order_id) REFERENCES orders(order_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
    """,
    "reviews": """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            customer_id INTEGER,
            rating INTEGER,
            review_text TEXT,
            review_date TEXT,
            FOREIGN KEY(product_id) REFERENCES products(product_id),
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        );
    """,
}

SQL_INDEXES: List[str] = [
    "CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);",
    "CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);",
    "CREATE INDEX IF NOT EXISTS idx_items_order ON order_items(order_id);",
    "CREATE INDEX IF NOT EXISTS idx_items_product ON order_items(product_id);",
    "CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);",
    "CREATE INDEX IF NOT EXISTS idx_reviews_customer ON reviews(customer_id);",
]


# HELPER FUNCTIONS 

def ensure_dir(path: str) -> None:
    """Ensure a directory exists."""
    os.makedirs(path, exist_ok=True)

def read_csv_rows(path: str) -> Iterable[dict]:
    """Read CSV rows into dictionaries."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        yield from reader

def insert_rows(conn: sqlite3.Connection, table: str, rows: Iterable[dict], columns: List[str]) -> None:
    """Insert multiple rows into a SQLite table."""
    placeholders = ",".join(["?"] * len(columns))
    colnames = ",".join(columns)
    sql = f"INSERT OR REPLACE INTO {table} ({colnames}) VALUES ({placeholders})"
    cur = conn.cursor()
    cur.executemany(sql, ([row.get(c, None) for c in columns] for row in rows))

def create_schema(conn: sqlite3.Connection) -> None:
    """Create tables and indexes in the database."""
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    for ddl in SQL_CREATE.values():
        cur.executescript(ddl)
    for idx in SQL_INDEXES:
        cur.execute(idx)
    conn.commit()


# MAIN INGESTION  #

def ingest(data_dir: str, db_path: str, replace: bool = False, write_ltv: bool = False) -> None:
    """Ingest all CSVs into SQLite database."""
    ensure_dir(data_dir)
    ensure_dir(os.path.dirname(db_path) or ".")

    if replace and os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Removed old database: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA foreign_keys = ON;")

    create_schema(conn)

    paths = {
        "customers": os.path.join(data_dir, "customers.csv"),
        "products": os.path.join(data_dir, "products.csv"),
        "orders": os.path.join(data_dir, "orders.csv"),
        "order_items": os.path.join(data_dir, "order_items.csv"),
        "reviews": os.path.join(data_dir, "reviews.csv"),
    }

    col_map = {
        "customers": ["customer_id", "name", "email", "address", "join_date"],
        "products": ["product_id", "name", "category", "price", "sku"],
        "orders": ["order_id", "customer_id", "order_date", "total", "status"],
        "order_items": ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "line_total"],
        "reviews": ["review_id", "product_id", "customer_id", "rating", "review_text", "review_date"],
    }

    try:
        for table, path in paths.items():
            if not os.path.exists(path):
                print(f"⚠️ {path} not found — skipping {table}")
                continue

            rows = list(read_csv_rows(path))
            if not rows:
                print(f"⚠️ No rows found in {path}; skipping.")
                continue

            # Type conversions for numeric fields
            for r in rows:
                for col in ["customer_id", "product_id", "order_id", "order_item_id", "rating", "quantity"]:
                    if col in r and r[col]:
                        try:
                            r[col] = int(float(r[col]))
                        except ValueError:
                            pass
                for col in ["price", "unit_price", "line_total", "total"]:
                    if col in r and r[col]:
                        try:
                            r[col] = float(r[col])
                        except ValueError:
                            pass

            with conn:
                insert_rows(conn, table, rows, col_map[table])
            print(f" Inserted {len(rows):>5} rows into {table}")

        # Update total order amounts
        with conn:
            conn.execute("""
                UPDATE orders
                SET total = (
                    SELECT ROUND(SUM(line_total), 2)
                    FROM order_items
                    WHERE order_items.order_id = orders.order_id
                )
                WHERE order_id IN (SELECT DISTINCT order_id FROM order_items);
            """)

        # Optional: Generate Customer Lifetime Value report
        if write_ltv:
            ltv_path = os.path.join(data_dir, "customer_ltv.csv")
            cur = conn.cursor()
            cur.execute("""
                SELECT
                    c.customer_id,
                    c.name,
                    COALESCE(SUM(o.total), 0) AS lifetime_spend,
                    COALESCE(COUNT(DISTINCT o.order_id), 0) AS orders_count,
                    CASE
                        WHEN COUNT(DISTINCT o.order_id) = 0 THEN 0
                        ELSE ROUND(SUM(o.total) / COUNT(DISTINCT o.order_id), 2)
                    END AS avg_order_value,
                    MAX(o.order_date) AS last_order_date
                FROM customers c
                LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
                GROUP BY c.customer_id, c.name
                ORDER BY lifetime_spend DESC;
            """)
            rows = cur.fetchall()
            headers = [d[0] for d in cur.description]
            with open(ltv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            print(f" Wrote Customer LTV report → {ltv_path}")

    finally:
        conn.close()
        print(f"\n Ingestion complete. Database ready at: {db_path}")


# ENTRYPOINT    

def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest synthetic e-commerce CSVs into SQLite database.")
    parser.add_argument("--data-dir", default=os.path.join(os.path.dirname(__file__), "..", "synthetic_ecom_data"))
    parser.add_argument("--db-path", default=os.path.join(os.path.dirname(__file__), "..", "database", "ecommerce.db"))
    parser.add_argument("--replace", action="store_true", help="Remove existing DB before ingestion")
    parser.add_argument("--ltv", dest="write_ltv", action="store_true", help="Generate customer_ltv.csv report")
    args = parser.parse_args()

    data_dir = os.path.normpath(args.data_dir)
    db_path = os.path.normpath(args.db_path)

    ensure_dir(os.path.dirname(db_path))
    ingest(data_dir, db_path, replace=args.replace, write_ltv=args.write_ltv)

if __name__ == "__main__":
    main()
