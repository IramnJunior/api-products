from pydantic import BaseModel
from typing import Union

class Product(BaseModel):
    name: str
    description: str
    price: float
    tax: float
    sale_price: Union[float, None] = None

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