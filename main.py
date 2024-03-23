from fastapi import FastAPI
import uvicorn
from database import connect_database, create_products_table
from models import Product


app = FastAPI()


con, cur = connect_database()

create_products_table(cur)


def get_sale_price(product: Product):
    sale_price = product.price + product.tax
    return sale_price


@app.get("/products/list")
async def list_products():
    sql = "SELECT * FROM products"
    cur.execute(sql)

    rows = cur.fetchall()

    return rows


@app.post("/products/add/")
async def add_product(product: Product):
    product_dict = product.model_dump()
    product_dict.update({"sale_price": round(get_sale_price(product), 2)})


    _, values = zip(*product_dict.items())

    sql = """INSERT INTO products (
             name, 
             description, 
             price, 
             tax, 
             sale_price
        )    
             VALUES (?, ?, ?, ?, ?)
    """
    cur.execute(sql, values)

    try:
        con.commit()
        return print("Query executed successfully")
    except: 
        return print("Query run failed")


@app.put("/products/edit/{id}")
async def edit_product(product: Product, id: int):
    product_dict = product.model_dump()
    product_dict.update({"sale_price": round(get_sale_price(product), 2)})

    _, values = zip(*product_dict.items())

    sql = f"""
    UPDATE products 
    SET name = ?, 
        description = ?, 
        price = ?, 
        tax = ?, 
        sale_price = ? 
        WHERE id = {id}
    """
    cur.execute(sql, values)

    try:
        con.commit()
        return print("Query executed successfully")
    except: 
        return print("Query run failed")


@app.delete("/products/delete/{id}")
async def delete_product(id: int):
    sql = f"""DELETE FROM products 
              WHERE id = {id}
        """
    cur.execute(sql)

    try:
        con.commit()
        return print("Query executed successfully")
    except: 
        return print("Query run failed")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)