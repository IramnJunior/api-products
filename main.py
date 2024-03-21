from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

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


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ksienedine777!",
    database="products"
)

mycursor = mydb.cursor()


#//////////////////////////////////////////////////////////////////////////////////////




def get_sale_price(product: Product):
    sale_price = product.price + product.tax
    return sale_price



@app.post("/products/add/")
async def add_product(product: Product):
    product_dict = product.model_dump()

    product_dict.update({"sale_price": f"{get_sale_price(product) :.2f}",})
    
    keys, values = zip(*product_dict.items())

    sql = f"INSERT INTO db {keys} VALUES (%s, %s, %s, %s, %s)"
    val = values
    
    mycursor.execute(sql, val)

    return mydb.commit()



@app.put("/products/edit/{id}")
async def edit_product(product: Product, id: int):
    product_dict = product.model_dump()

    product_dict.update({"sale_price": f"{get_sale_price(product) :.2f}",})

    _, values = zip(*product_dict.items())

    sql = f"UPDATE db SET name = %s, description = %s, price = %s, tax = %s, sale_price = %s WHERE iddb = {id}"
    val = values

    mycursor.execute(sql, val)

    return mydb.commit() 



@app.delete("/products/delete/{id}")
async def delete_product(id: int):
    sql = f"DELETE FROM db WHERE iddb = {id}"

    mycursor.execute(sql)
    return mydb.commit()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)