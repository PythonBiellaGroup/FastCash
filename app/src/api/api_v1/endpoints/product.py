from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Any

from app.src.models.api.product import ProductRead, ProductCreate, ProductUpdate
from app.src.db.engine import get_db
from app.src.db.manager import get_session
from app.src.models.db.product import Product


router = APIRouter()


@router.get("/", response_model=List[ProductRead])
def read_all_products(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> Any:
    """
    Retrieve items.
    """
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return products


@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate) -> Any:
    engine = get_db()
    with Session(engine) as session:
        db_product = Product.from_orm(product)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product


@router.get("/{name}", response_model=ProductRead)
def read_product_name(product_name: str) -> Any:
    engine = get_db()
    with Session(engine) as session:
        product = session.get(Product, product_name)
        if not product:
            raise HTTPException(status_code=404, detail="Item not found")
        return product


@router.patch("/{product_id}", response_model=ProductRead)
def update_hero_id(product_id: int, product: ProductUpdate):
    engine = get_db()
    with Session(engine) as session:
        db_product = session.get(Product, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        hero_data = product.dict(exclude_unset=True)
        for key, value in hero_data.items():
            setattr(db_product, key, value)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product


@router.patch("/{name}", response_model=ProductRead)
def update_hero_name(product_name: int, product: ProductUpdate):
    engine = get_db()
    with Session(engine) as session:
        db_product = session.get(Product, product_name)
        if not db_product:
            raise HTTPException(
                status_code=404, detail="Product not found, impossible to update"
            )
        hero_data = product.dict(exclude_unset=True)  # to use the nullable data
        for key, value in hero_data.items():
            setattr(db_product, key, value)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product


@router.delete("/{product_id}")
def delete_hero(product_id: int):
    engine = get_db()
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(
                status_code=404, detail="Product not found, impossible to remove"
            )
        session.delete(product)
        session.commit()
        return {"ok": True}
