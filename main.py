from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import os
from dotenv import find_dotenv, load_dotenv

import mysql.connector


app = FastAPI()


class Product(BaseModel):
    name: str
    description: str
    price: float
    tax: float
    sale_price: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Vodka",
                    "description": "Bebida Alcoolica",
                    "price": 11.00,
                    "tax": 2.99
                }
            ]
        }
    }



#/////////////////////////////////////////////////////////////////////////////////////

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


def connect_db():
    try:
        mydb = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME")
        )
        mycursor = mydb.cursor()
        return mydb, mycursor
    except: return print("error connecting to database")

#//////////////////////////////////////////////////////////////////////////////////////



def get_sale_price(product: Product):
    sale_price = product.price + product.tax
    return sale_price



@app.post("/products/add/")
async def add_product(product: Product):
    product_dict = product.model_dump()
    product_dict.update({"sale_price": round(get_sale_price(product), 2)})


    _, values = zip(*product_dict.items())

    sql = "INSERT INTO products (name, description, price, tax, sale_price) VALUES (%s, %s, %s, %s, %s)"
    mydb, mycursor = connect_db()
    mycursor.execute(sql, values)

    try:
        mydb.commit()
        return print("Quarry executed successfully")
    except: return print("Quarry run failed")



@app.put("/products/edit/{id}")
async def edit_product(product: Product, id: int):
    product_dict = product.model_dump()
    product_dict.update({"sale_price": round(get_sale_price(product), 2)})

    _, values = zip(*product_dict.items())

    sql = f"UPDATE products SET name = %s, description = %s, price = %s, tax = %s, sale_price = %s WHERE id = {id}"
    mydb, mycursor = connect_db()
    mycursor.execute(sql, values)

    try:
        mydb.commit()
        return print("Quarry executed successfully")
    except: return print("Quarry run failed")



@app.delete("/products/delete/{id}")
async def delete_product(id: int):
    sql = f"DELETE FROM products WHERE id = {id}"
    mydb, mycursor = connect_db()
    mycursor.execute(sql)

    try:
        mydb.commit()
        return print("Quarry executed successfully")
    except: print("Quarry run failed")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)