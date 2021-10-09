from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List

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
    *, session: AsyncSession = Depends(get_session), producttype_id: int = Path(..., ge=1)
):
    try:
        result = await session.execute(select(ProductType).where(ProductType.id == producttype_id))
        db_pt = result.scalars().first()
        if db_pt:
            return db_pt
        else:
            raise HTTPException(status_code=404, detail="Product type not found")
    except KeyError:
        raise HTTPException(status_code=400, detail="Product type not found")


@router.get("/", response_model=List[ProductTypeRead])
async def read_product_types(
    *,
    session: AsyncSession = Depends(get_session)
):
    """
    Get all the existing product types
    """
    result = await session.execute(select(ProductType))
    product_types = result.scalars().all()
    return product_types


@router.get("/{producttype_id}", response_model=ProductTypeRead)
async def read_product_type(*, db_pt: ProductType = Depends(get_producttype_or_404)):
    """
    Get the product type by id
    """
    return db_pt


@router.post("/", response_model=ProductTypeRead)
async def create_product_type(
    *, session: AsyncSession = Depends(get_session), product_type: ProductTypeCreate
):
    """
    Create a product type
    """
    try:
        db_pt = ProductType(name=product_type.name, description=product_type.description)
        session.add(db_pt)
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=404, detail="Impossible to create product type with same name"
        )
    await session.flush(db_pt)
    return db_pt


@router.patch("/{producttype_id}", response_model=ProductTypeRead)
async def update_product_type(
    *,
    session: AsyncSession = Depends(get_session),
    db_pt: ProductType = Depends(get_producttype_or_404),
    pt: ProductTypeUpdate
):
    """
    Modify a product type
    """
    # exclude_unset=True: it would only include the values
    # that were sent by the client
    pt_data = pt.dict(exclude_unset=True)
    for key, value in pt_data.items():
        setattr(db_pt, key, value)
    session.add(db_pt)
    await session.commit()
    await session.flush(db_pt)
    return db_pt


@router.delete("/{producttype_id}")
async def delete_product_type(
    *,
    session: AsyncSession = Depends(get_session),
    db_pt: ProductType = Depends(get_producttype_or_404)
):
    """
    Delete and remove an existing product type by id; it must be >= 1
    """
    await session.delete(db_pt)
    await session.commit()
    await session.flush(db_pt)
    return {"ok": True}
