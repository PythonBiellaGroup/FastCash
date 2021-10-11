from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from typing import List
import datetime as dt


from app.src.common.security import get_current_user
from app.src.common.utils import profiling_api
from app.src.models.app_user import AppUser
from app.src.models.product_type import (
    ProductType,
    ProductTypeRead,
    ProductTypeCreate,
    ProductTypeUpdate,
)
from app.src.db.engine import get_session

router = APIRouter()


# A scopo didattico inserita la validazione di producttype_id con Path:
# - non potrà essere < 1
async def get_producttype_or_404(
    *,
    session: Session = Depends(get_session),
    producttype_id: int = Path(..., ge=1),
    current_user: AppUser = Depends(get_current_user),
):
    start_time = dt.datetime.now()
    try:
        db_pt = session.get(ProductType, producttype_id)
        if db_pt:
            return {
                "db_pt": db_pt,
                "username": current_user.username,
                "start_time": start_time,
            }
        else:
            raise HTTPException(status_code=404, detail="Product type not found")
    except KeyError:
        raise HTTPException(status_code=400, detail="Product type not found")


@router.get("/", response_model=List[ProductTypeRead])
# lte -> less than or equal
async def read_product_types(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    current_user: AppUser = Depends(get_current_user),
):
    """
    Get all the existing product types
    """
    start_time = dt.datetime.now()
    product_types = session.exec(select(ProductType).offset(offset).limit(limit)).all()
    profiling_api("ProductType:get:all", start_time, current_user.username)
    return product_types


@router.get("/{producttype_id}", response_model=ProductTypeRead)
async def read_product_type(
    *, producttype_id: int, db_pt: ProductType = Depends(get_producttype_or_404)
):
    """
    Get the product type by id
    """
    profiling_api(
        f"ProductType:read:by_id:{producttype_id}",
        db_pt["start_time"],
        db_pt["username"],
    )
    return db_pt["db_pt"]


@router.post("/", response_model=ProductTypeRead)
async def create_product_type(
    *,
    session: Session = Depends(get_session),
    product_type: ProductTypeCreate,
    current_user: AppUser = Depends(get_current_user),
):
    """
    Create a product type
    """
    start_time = dt.datetime.now()
    try:
        db_pt = ProductType.from_orm(product_type)
        session.add(db_pt)
        session.commit()
        session.refresh(db_pt)
    except IntegrityError:
        raise HTTPException(
            status_code=404, detail="Impossible to create product type with same name"
        )
    profiling_api("ProductType:insert:single", start_time, current_user.username)
    return db_pt


@router.patch("/{producttype_id}", response_model=ProductTypeRead)
async def update_product_type(
    *,
    producttype_id: int,
    session: Session = Depends(get_session),
    pt: ProductTypeUpdate,
    db_pt: ProductType = Depends(get_producttype_or_404),
):
    """
    Modify a product type
    """
    # exclude_unset=True: it would only include the values
    # that were sent by the client
    existing_pt = db_pt["db_pt"]
    pt_data = pt.dict(exclude_unset=True)
    for key, value in pt_data.items():
        setattr(existing_pt, key, value)
    session.add(existing_pt)
    session.commit()
    session.refresh(existing_pt)
    profiling_api(
        f"ProductType:update:by_id:{producttype_id}",
        db_pt["start_time"],
        db_pt["username"],
    )
    return existing_pt


@router.delete("/{producttype_id}")
async def delete_product_type(
    *,
    producttype_id: int,
    session: Session = Depends(get_session),
    db_pt: ProductType = Depends(get_producttype_or_404),
):
    """
    Delete and remove an existing product type by id; it must be >= 1
    """
    existing_db_pt = db_pt["db_pt"]
    session.delete(existing_db_pt)
    session.commit()
    profiling_api(
        f"ProductType:delete:by_id:{producttype_id}",
        db_pt["start_time"],
        db_pt["username"],
    )
    return {"ok": True}
