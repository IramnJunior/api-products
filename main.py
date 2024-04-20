from fastapi import FastAPI, Request
from os import getenv
import uvicorn

from connect_database import supabase
from helpers import get_sale_price, get_table_data
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

app.mount("/templates/style", StaticFiles(directory="templates/style"), name="style")
app.mount("/templates/scripts", StaticFiles(directory="templates/scripts"), name="scripts")

templates = Jinja2Templates(directory="templates")


@app.get("/home/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/home/products", response_class=HTMLResponse)
async def home_products(request: Request):
    return templates.TemplateResponse(
        request=request, name="home-products.html"
    )


@app.get("/get/credentials/")
async def get_user_and_password():
    data = get_table_data("Logins")
    return data


@app.get("/get/products/")
async def get_products():
    data = get_table_data("products-db")
    return data


@app.post("/add/")
async def add_product(product: Product):
    product_dict = product.model_dump()
    product_dict.update({"sale_price": round(get_sale_price(product), 2)})

    try:
        supabase.table("products-db").insert(product_dict).execute()
        return print("Query executed successfully")
    except ValueError: 
        return print("Query run failed")


@app.put("/edit/{id}")
async def edit_product(product: Product, id: int):
    product_dict = product.model_dump()
    product_dict.update({"sale_price": round(get_sale_price(product), 2)})

    try:
        supabase.table("products-db").update(product_dict).eq("id", id).execute()
        return print("Query executed successfully")
    except: 
        return print("Query run failed")


@app.delete("/delete/{id}")
async def delete_product(id: int):
    try:
        supabase.table("products-db").delete().eq("id", id).execute()
        return print("Query executed successfully")
    except: 
        return print("Query run failed")


HOST = '0.0.0.0'
PORT = int(getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)