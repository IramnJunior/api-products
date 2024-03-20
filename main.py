from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI()


class Product(BaseModel):
    id: int | None = None
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

products_list = []


class AutoIncrementId:
    id = 0
    def __init__(self):
        AutoIncrementId.id += 1



def get_sale_price(product: Product):
    sale_price = product.price + product.tax
    return sale_price



def get_product_id():
    products_id = []

    for product in products_list:
        products_id.append(product["id"])

    return products_id



@app.get("/products")
async def get_products():
    return products_list



@app.post("/products/add/")
async def add_product(product: Product):
    product_dict = product.model_dump()

    product_dict.update({
        "sale_price": f"{get_sale_price(product) :.2f}",
        "id": AutoIncrementId().id
        })

    products_list.append(product_dict)
    return products_list



@app.put("/products/edit/{id}")
async def edit_product(product: Product, id: int):
    product_dict = product.model_dump()

    product_dict.update({
        "sale_price": f"{get_sale_price(product) :.2f}",
        "id": id
        })

    product_id = get_product_id()

    products_list[product_id.index(id)] = product_dict

    return products_list



@app.delete("/products/delete/{id}")
async def delete_product(id: int):
    product_id = get_product_id()

    del products_list[product_id.index(id)]

    return products_list



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)