from models import Product
from connect_database import supabase

def get_sale_price(product: Product):
    sale_price = product.price + product.tax
    return sale_price


def get_table_data(table_name: str):
    request = supabase.table(table_name).select("*").execute()
    request_dict = dict(request)
    data = request_dict["data"]
    return data