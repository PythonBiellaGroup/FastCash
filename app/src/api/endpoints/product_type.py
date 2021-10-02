from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session, select
from typing import List, Any

from app.src.models.product_type import ProductType, ProductTypeRead, ProductTypeCreate, ProductTypeUpdate
from app.src.db.engine import get_session

router = APIRouter()


# A scopo didattico inserita la validazione di producttype_id con Path:
# - non potrà essere < 1
async def get_producttype_or_404(*, session: Session = Depends(get_session),
                      producttype_id: int = Path(..., ge=1)):
    try:
        db_pt = session.get(ProductType, producttype_id)
        if db_pt:
            return db_pt
        else:
            raise HTTPException(status_code=404, detail="Product type not found")    
    except KeyError:
        raise HTTPException(status_code=400, detail="Product type not found")


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


@router.get("/{producttype_id}", response_model=ProductTypeRead)
async def read_product_type(*, db_pt: ProductType = Depends(get_producttype_or_404)):
    """
    Get the product type by id
    """
    return db_pt


@router.post("/", response_model=ProductTypeRead)
async def create_product_type(*, session: Session = Depends(get_session),
                        product_type: ProductTypeCreate):
    """
    Create a product type
    """
    db_pt = ProductType.from_orm(product_type)
    session.add(db_pt)
    session.commit()
    session.refresh(db_pt)
    return db_pt


@router.patch("/{producttype_id}", response_model=ProductTypeRead)
async def update_product_type(*, session: Session = Depends(get_session),
                              db_pt: ProductType = Depends(get_producttype_or_404),
                              pt: ProductTypeUpdate):
    """
    Modify a product type
    """
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
                              db_pt: ProductType = Depends(get_producttype_or_404)):
    """
    Delete and remove an existing product type by id; it must be >= 1
    """
    session.delete(db_pt)
    session.commit()
    return {"ok": True}
