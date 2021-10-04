from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select

from live.src.db.manager import get_session
from live.src.logger import logger
from live.src.models.product import Product, ProductRead, ProductCreate


router = APIRouter()


@router.get("/", response_model=List[ProductRead])
def get_products(
    session: Session = Depends(get_session), limit: int = Query(default=100, lte=100)
):

    logger.info("Get all products")
    products = session.exec(select(Product).limit(limit)).all()
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products


@router.get("/id", response_model=ProductRead)
def get_one_products(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/name", response_model=ProductRead)
def get_one_products_by_name(
    product_name: str, session: Session = Depends(get_session)
):
    product = session.get(Product, product_name)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductRead)
def insert_product(product: ProductCreate, session: Session = Depends(get_session)):
    try:
        logger.info(f"Inserimento nuovo prodotto: {product.name}")
        db_product = Product.from_orm(product)
        session.add(db_product)
        session.commit()
    except Exception as e:
        logger.error(f"Impossibile creare il nuovo prodotto: {e}")
        logger.exception(e)
        raise HTTPException(
            status_code=400, detail="Impossible to create the new product"
        )

    return db_product


# @app.delete("/products/{product_id}", response_model=Product)
# def delete_product(product_id: int):
#     deleted_product = product_db[product_id]
#     product_db.pop(product_id)
#     print(product_db)
#     return deleted_product


# @app.put("/products/{product_id}", response_model=Product)
# def modify_product(product_id: int, product: Product):
#     product_db[product_id] = product
#     print(product_db)
#     return product
