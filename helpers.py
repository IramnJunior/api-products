from database import connect_database
from models import Product

con, cur = connect_database()

def get_sale_price(product: Product):
    sale_price = product.price + product.tax
    return sale_price


def get_column_products():
    sql = "SELECT * FROM products"
    data = cur.execute(sql)

    products_column = []
    
    for column in data.description:
        products_column.append(column[0])
    return products_column


def get_row_products():
    sql = "SELECT * FROM products"
    data = cur.execute(sql)

    products_row = []

    for row in data:
        products_row.append(row)
    return products_row


def convert_array_to_dict(products_row, products_column):
    products = []
    for row in products_row:
        products_dict = {}
        index = 0
        while index < 6:
            products_dict[products_column[index]] = row[index]
            index += 1
        products.append(products_dict)
    return products