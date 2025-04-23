import sqlite3


def create_database():
    connection = sqlite3.connect("shop.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   price REAL,
                   stock INTEGER
                   )
                """)

    # Beispielprodukte
    cursor.execute(
        "INSERT INTO products (name, price, stock) VALUES ('Laptop', 999.99, 5)")
    cursor.execute(
        "INSERT INTO products (name, price, stock) VALUES ('Smartphone', 599.49, 10)")
    cursor.execute(
        "INSERT INTO products (name, price, stock) VALUES('Kopfhörer', 199.99, 20)")

    connection.commit()
    connection.close()


create_database()
