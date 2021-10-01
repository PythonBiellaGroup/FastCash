from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session, select
from typing import List, Any

from app.src.models.product_type import ProductType, ProductTypeRead, ProductTypeCreate, ProductTypeUpdate
from app.src.db.engine import get_session

router = APIRouter()


@router.get("/", response_model=List[ProductTypeRead])
# lte -> less than or equal
async def read_product_types(*, session: Session = Depends(get_session),
                       offset: int = 0,
                       limit: int = Query(default=100, lte=100)):
    """
    Get all the existing product types
    """
    product_types = session.exec(
        select(ProductType).offset(offset).limit(limit)).all()
    return product_types

# A scopo didattico inserita la validazione di producttype_id con Path:
# - non potrà essere < 1
@router.get("/{producttype_id}", response_model=ProductTypeRead)
async def read_product_type(*, session: Session = Depends(get_session),
                      producttype_id: int = Path(..., ge=1)):
    """
    Get the product type by id
    """
    pt = session.get(ProductType, producttype_id)
    if not pt:
        raise HTTPException(
            status_code=404,
            detail="Product type not found"
            )
    return pt



@router.post("/", response_model=ProductTypeRead)
async def create_product_type(*, session: Session = Depends(get_session),
                        product_type: ProductTypeCreate):
    """
    Add a product type
    """
    db_pt = ProductType.from_orm(product_type)
    session.add(db_pt)
    session.commit()
    session.refresh(db_pt)
    return db_pt


@router.patch("/{producttype_id}", response_model=ProductTypeRead)
async def update_product_type(*, session: Session = Depends(get_session),
                        producttype_id: int, pt: ProductTypeUpdate):
    """
    Modify a product type
    """
    db_pt = session.get(ProductType, producttype_id)
    if not db_pt:
        raise HTTPException(status_code=404, detail="Product type found")
    # exclude_unset=True: it would only include the values
    # that were sent by the client
    pt_data = pt.dict(exclude_unset=True)
    for key, value in pt_data.items():
        setattr(db_pt, key, value)
    session.add(db_pt)
    session.commit()
    session.refresh(db_pt)
    return db_pt


@router.delete("/{producttype_id}")
async def delete_product_type(*, session: Session = Depends(get_session),
                        producttype_id: int = Path(..., ge=1)):
    """
    Delete and remove an existing product type by id; it must be >= 1
    """
    pt = session.get(ProductType, producttype_id)
    if not pt:
        raise HTTPException(
            status_code=404,
            detail="Product type not found"
            )
    session.delete(pt)
    session.commit()
    return {"ok": True}

