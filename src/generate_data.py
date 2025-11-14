"""
Synthetic E-commerce Data Generator
-----------------------------------

Generates realistic e-commerce datasets for analytics or pipeline testing.

Creates five CSV files in the `synthetic_ecom_data/` folder:
- customers.csv
- products.csv
- orders.csv
- order_items.csv
- reviews.csv

Usage Example:
    python src/generate_data.py --seed 42 --scale 1

Arguments:
    --seed   : Random seed for reproducibility
    --scale  : Multiplies dataset size (e.g., 2 → doubles all rows)

"""
import argparse
import os
from datetime import datetime
import numpy as np
import pandas as pd
from faker import Faker

# ---------------------------- Helpers ----------------------------

def ensure_dir(path: str) -> None:
    """Create directory if it doesn’t exist."""
    os.makedirs(path, exist_ok=True)



# ---------------------------- Data Generators ----------------------------

def generate_customers(fake: Faker, n_customers: int) -> pd.DataFrame:
    """Generate synthetic customer records."""
    customers = []
    for cid in range(1, n_customers + 1):
        name = fake.name()
        email = fake.unique.email()
        join_date = fake.date_between(start_date='-3y', end_date='today')
        customers.append({
            'customer_id': cid,
            'name': name,
            'email': email,
            'address': fake.address().replace('\n', ', '),
            'join_date': join_date.isoformat(),
        })
    return pd.DataFrame(customers)


def generate_products(fake: Faker, n_products: int) -> pd.DataFrame:
    """Generate synthetic product catalog."""
    categories = ['Electronics', 'Home', 'Books', 'Toys', 'Clothing', 'Sports', 'Beauty']
    products = []
    for pid in range(1, n_products + 1):
        category = np.random.choice(categories, p=[0.18,0.14,0.12,0.12,0.18,0.14,0.12])
        price = round(float(np.random.lognormal(mean=3.0, sigma=0.8)), 2)
        name = f"{fake.word().capitalize()} {fake.word().capitalize()}"
        sku = f"SKU-{pid:06d}"
        products.append({
            'product_id': pid,
            'name': name,
            'category': category,
            'price': price,
            'sku': sku,
        })
    return pd.DataFrame(products)


def generate_orders_and_items(fake: Faker, n_orders: int, customers_df: pd.DataFrame, products_df: pd.DataFrame):
    """Generate synthetic orders and related order items."""
    orders = []
    items = []
    order_id = 1
    for _ in range(n_orders):
        cust_id = int(np.random.choice(customers_df['customer_id']))
        order_date = fake.date_time_between(start_date='-2y', end_date='now')
        n_items = np.random.randint(1, 6)
        chosen_products = products_df.sample(n=n_items, replace=False)
        total = 0.0
        for _, prod in chosen_products.iterrows():
            qty = int(np.random.choice([1,1,1,2,3]))
            unit_price = float(prod['price'])
            line_total = round(unit_price * qty, 2)
            items.append({
                'order_item_id': len(items) + 1,
                'order_id': order_id,
                'product_id': int(prod['product_id']),
                'quantity': qty,
                'unit_price': unit_price,
                'line_total': line_total,
            })
            total += line_total
        status = np.random.choice(['completed', 'shipped', 'cancelled', 'returned'], p=[0.7,0.2,0.06,0.04])
        orders.append({
            'order_id': order_id,
            'customer_id': cust_id,
            'order_date': order_date.isoformat(sep=' '),
            'total': round(total, 2),
            'status': status,
        })
        order_id += 1
    return pd.DataFrame(orders), pd.DataFrame(items)


def generate_reviews(fake: Faker, customers_df: pd.DataFrame, products_df: pd.DataFrame, n_reviews: int) -> pd.DataFrame:
    """Generate synthetic product reviews."""
    reviews = []
    for rid in range(1, n_reviews + 1):
        product_id = int(np.random.choice(products_df['product_id']))
        customer_id = int(np.random.choice(customers_df['customer_id']))
        rating = int(np.random.choice([1,2,3,4,5], p=[0.05,0.05,0.15,0.4,0.35]))
        text = fake.sentence(nb_words=12)
        review_date = fake.date_time_between(start_date='-2y', end_date='now')
        reviews.append({
            'review_id': rid,
            'product_id': product_id,
            'customer_id': customer_id,
            'rating': rating,
            'review_text': text,
            'review_date': review_date.isoformat(sep=' '),
        })
    return pd.DataFrame(reviews)

# ---------------------------- Main ----------------------------

def main():
    parser = argparse.ArgumentParser(description='Generate synthetic e-commerce datasets')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale factor; multiplies base sizes')
    args = parser.parse_args()

    # Setup
    outdir = os.path.join(os.path.dirname(__file__), '..', 'synthetic_ecom_data')
    outdir = os.path.normpath(outdir)
    ensure_dir(outdir)

    # Seed reproducibility
    fake = Faker()
    Faker.seed(args.seed)
    np.random.seed(args.seed)

    # Base sizes
    base_customers = 500
    base_products = 200
    base_orders = 2500
    base_reviews = 800

    n_customers = int(base_customers * args.scale)
    n_products = int(base_products * args.scale)
    n_orders = int(base_orders * args.scale)
    n_reviews = int(base_reviews * args.scale)

    # Generate all datasets
    customers_df = generate_customers(fake, n_customers)
    products_df = generate_products(fake, n_products)
    orders_df, items_df = generate_orders_and_items(fake, n_orders, customers_df, products_df)
    reviews_df = generate_reviews(fake, customers_df, products_df, n_reviews)

     # Save as CSV
    customers_df.to_csv(os.path.join(outdir, 'customers.csv'), index=False)
    products_df.to_csv(os.path.join(outdir, 'products.csv'), index=False)
    orders_df.to_csv(os.path.join(outdir, 'orders.csv'), index=False)
    items_df.to_csv(os.path.join(outdir, 'order_items.csv'), index=False)
    reviews_df.to_csv(os.path.join(outdir, 'reviews.csv'), index=False)

    print("\n Synthetic Ecom Data Generated Successfully!")
    print(f"Output Directory: {outdir}")
    print(f"Customers: {len(customers_df)}, items: {len(items_df)}, orders: {len(orders_df)}, products: {len(products_df)}, reviews: {len(reviews_df)}")

if __name__ == '__main__':
    main()
