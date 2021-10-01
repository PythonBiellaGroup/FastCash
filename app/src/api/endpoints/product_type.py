from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Any

from app.src.models.product_type import ProductType, ProductTypeRead, ProductTypeCreate, ProductTypeReadwithProduct
from app.src.db.engine import get_db
from app.src.db.manager import get_session


router = APIRouter()


@router.get("/", response_model=List[ProductTypeRead])
# lte -> less than or equal
def read_product_types(*, session: Session = Depends(get_session),
                       offset: int = 0,
                       limit: int = Query(default=100, lte=100)):
    product_types = session.exec(
        select(ProductType).offset(offset).limit(limit)).all()
    return product_types


@router.post("/", response_model=ProductTypeRead)
def create_product_type(*, session: Session = Depends(get_session),
                        product_type: ProductTypeCreate):
    db_pt = ProductType.from_orm(product_type)
    session.add(db_pt)
    session.commit()
    session.refresh(db_pt)
    return db_pt