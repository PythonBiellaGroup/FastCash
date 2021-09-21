import os
import fastapi
import uvicorn
from typing import Optional
from pydantic import BaseModel

app = fastapi.FastAPI()

product_db = {
    1: {
        "id": "1",
        "name": "kebab",
        "description": "senza cipolla",
        "price": 4.00,
        "available": True,
    },
    2: {
        "id": 2,
        "name": "hamburger",
        "description": "doppio bacon",
        "price": 6.00,
        "available": False,
    },
}


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    available: bool


@app.get("/")
def index():
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Ciao PythonBiellaGroup</h1>"
        "</body>"
        "</html>"
    )
    return fastapi.responses.HTMLResponse(content=body)


@app.get("/products/")
def get_products():
    return product_db


@app.get("/products/{product_id}", response_model=Product)
def get_one_products(product_id: int):
    return product_db[product_id]


@app.post("/products/", response_model=Product)
def insert_product(product: Product):
    product_db[product.id] = product
    print(product_db)
    return product


@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int):
    deleted_product = product_db[product_id]
    product_db.pop(product_id)
    print(product_db)
    return deleted_product


@app.put("/products/{product_id}", response_model=Product)
def modify_product(product_id: int, product: Product):
    product_db[product_id] = product
    print(product_db)
    return product


if __name__ == "__main__":
    port = int(os.environ.get("API_ENDPOINT_PORT", "8000"))
    host = os.environ.get("API_ENDPOINT_HOST", "127.0.0.1")

    uvicorn.run("main:api", port=port, host=host, reload=True)
