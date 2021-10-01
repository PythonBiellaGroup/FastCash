from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session, select
from typing import List, Any

from app.src.models.product import Product, ProductRead, ProductCreate, ProductUpdate, ProductReadwithType
from app.src.db.engine import get_db
from app.src.db.manager import get_session


router = APIRouter()


@router.get("/", response_model=List[ProductRead])
async def read_all_products(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> Any:
    """
    Retrieve all products
    """
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return products


# @router.get("/products/", response_model=List[ProductReadwithType])
# def read_all_products_type(
#     session: Session = Depends(get_session),
#     offset: int = 0,
#     limit: int = Query(default=100, lte=100),
# ) -> Any:
#     """
#     Retrieve items.
#     """
#     products = session.exec(select(Product).offset(offset).limit(limit)).all()
#     return products


@router.post("/", response_model=ProductRead)
async def create_product(product: ProductCreate) -> Any:
    """
    Create a new single product
    """
    engine = get_db()
    with Session(engine) as session:
        db_product = Product.from_orm(product)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product


# @router.get("/{name}", response_model=ProductRead)
# def read_product_name(product_name: str) -> Any:
#     engine = get_db()
#     with Session(engine) as session:
#         product = session.get(Product, product_name)
#         if not product:
#             raise HTTPException(status_code=404, detail="Item not found")
#         return product


@router.patch("/update/{product_id}", response_model=ProductRead)
async def update_product_by_id(product_id: int, product: ProductUpdate):
    """
    Modify and existing product by id
    """
    engine = get_db()
    with Session(engine) as session:
        db_product = session.get(Product, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        pr_data = product.dict(exclude_unset=True)
        for key, value in pr_data.items():
            setattr(db_product, key, value)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product


@router.patch("/update/{name}", response_model=ProductRead)
async def update_product_by_name(product_name: int, product: ProductUpdate):
    """
    Modify an existing product by name
    """
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
async def delete_product(product_id: int = Path(..., ge=1)):
    """
    Delete and remove an existing product by id; it must be >= 1
    """
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
