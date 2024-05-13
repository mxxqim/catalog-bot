import sqlite3 as sq

db = sq.connect('database.db')
cur = db.cursor()


def connect_database():
    cur.execute("""CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_description TEXT,
    product_price INT,
    product_photo TEXT
    )""")
    db.commit()


async def select_product(product_id) -> dict:
    product = cur.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if not product:
        pass
    else:
        data = dict(zip(("id", "product_description", "product_price", "product_photo"), product))
        return data


async def select_count_products():
    data = cur.execute("SElECT COUNT(*) FROM products").fetchall()
    return data[0]


async def select_all_products():
    data = cur.execute("SELECT * FROM products").fetchall()
    return data


async def select_prodcut_for_rowid(rowid):
    data = cur.execute("SELECT * FROM products LIMIT 1 OFFSET ?", (rowid,)).fetchone()
    return data


async def insert_product(product_price, product_photo, product_description):
    cur.execute("INSERT INTO products(product_description, product_price, product_photo) VALUES(?, ?, ?)", (product_description, product_price, product_photo))
    db.commit()
