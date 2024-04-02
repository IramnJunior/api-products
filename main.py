from fastapi import FastAPI, Request
import uvicorn
from os import getenv

from database import connect_database, create_products_table
from helpers import get_sale_price, get_row_products, get_column_products, convert_array_to_dict
from models import Product

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

con, cur = connect_database()

create_products_table(cur)

app.mount("/templates/style", StaticFiles(directory="templates/style"), name="styles")

templates = Jinja2Templates(directory="templates")

@app.get("/", tags=["Root"], response_class=HTMLResponse)
async def list_products(request: Request):
    Product = convert_array_to_dict(get_row_products(), get_column_products())
    return templates.TemplateResponse(
        request=request, name="index.html", context={"products": Product}
    )


@app.post("/products/add/")
async def add_product(product: Product):
    product_dict = product.model_dump()
    product_dict.update({"sale_price": round(get_sale_price(product), 2)})

    sql = """
    INSERT INTO 
        products 
            (name, description, price, tax, sale_price)
        VALUES 
            (?, ?, ?, ?, ?)
    """ 
    _, values = zip(*product_dict.items())
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
        UPDATE 
            products 
        SET 
            name = ?, 
            description = ?, 
            price = ?, 
            tax = ?, 
            sale_price = ?  
        WHERE 
            id = {id}
    """
    cur.execute(sql, values)

    try:
        con.commit()
        return print("Query executed successfully")
    except: 
        return print("Query run failed")


@app.delete("/products/delete/{id}")
async def delete_product(id: int):
    sql = f"""
        DELETE FROM products 
        WHERE id = {id}
    """
    cur.execute(sql)

    try:
        con.commit()
        return print("Query executed successfully")
    except: 
        return print("Query run failed")


if __name__ == "__main__":
    port = int(getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)