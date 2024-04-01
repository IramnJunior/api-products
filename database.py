import sqlite3

def connect_database():
    try:
        con = sqlite3.connect("products.db")
        cur = con.cursor()
        print("successful database connection")
    except ValueError:
        print("unsuccessful database connection")
    return con, cur


def create_products_table(cur):
    sql = """
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(45),
            description VARCHAR(999),
            price FLOAT(5),
            tax FLOAT(5),
            sale_price FLOAT(5)
            )
    """
    try:
        cur.execute(sql)
        return print("table created successfully")
    except ValueError:
        return  print("table was not created due to an error")