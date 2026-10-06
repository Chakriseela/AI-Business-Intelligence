from pathlib import Path
import csv
import sqlite3

# BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "backend" / "database" / "business.db"

SCHEMA = '''
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    region TEXT NOT NULL,
    customer_segment TEXT NOT NULL
);

CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    cost REAL NOT NULL,
    stock_quantity INTEGER NOT NULL
);

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
'''


def load_table(conn, table, filename, converters=None):
    converters = converters or {}
    DATA_DIR = PROJECT_ROOT / "data"
    path = DATA_DIR / filename
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        rows = []
        for row in reader:
            for column, converter in converters.items():
                row[column] = converter(row[column])
            rows.append(tuple(row[column] for column in columns))

    placeholders = ','.join('?' for _ in columns)
    sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
    conn.executemany(sql, rows)
    return len(rows)


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')

    try:
        conn.executescript(SCHEMA)

        counts = {
            'customers': load_table(
                conn, 'customers', 'customers.csv'
            ),
            'products': load_table(
                conn, 'products', 'products.csv',
                {'price': float, 'cost': float, 'stock_quantity': int}
            ),
            'orders': load_table(
                conn, 'orders', 'orders.csv',
                {'total_amount': float}
            ),
            'order_items': load_table(
                conn, 'order_items', 'order_items.csv',
                {'quantity': int, 'unit_price': float}
            ),
        }

        conn.commit()

        fk_errors = conn.execute('PRAGMA foreign_key_check').fetchall()
        if fk_errors:
            raise RuntimeError(f'Foreign-key validation failed: {fk_errors[:5]}')

        mismatches = conn.execute('''
            SELECT o.order_id,
                   ROUND(o.total_amount, 2) AS stored_total,
                   ROUND(SUM(oi.quantity * oi.unit_price), 2) AS calculated_total
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            GROUP BY o.order_id
            HAVING ABS(stored_total - calculated_total) > 0.01
        ''').fetchall()

        if mismatches:
            raise RuntimeError(
                f'Order total validation failed for {len(mismatches)} orders. '
                f'First mismatches: {mismatches[:5]}'
            )

        print(f'Created: {DB_PATH}')
        print('Rows:', counts)
        print('Foreign-key violations: 0')
        print('Order total mismatches: 0')

    finally:
        conn.close()


if __name__ == '__main__':
    main()
