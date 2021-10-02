from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session, select
from typing import List, Any

from app.src.models.product import Product, ProductRead, ProductCreate, ProductUpdate, ProductReadwithTypeAndTags
from app.src.db.engine import get_session

# TODO Gestione dei tag di prodotto
router = APIRouter()

async def get_product_or_404(*, session: Session = Depends(get_session),
                      product_id: int = Path(..., ge=1)):
    try:
        return session.get(Product, product_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Product not found")


@router.get("/", response_model=List[ProductReadwithTypeAndTags])
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


@router.get("/{product_id}", response_model=ProductReadwithTypeAndTags)
async def read_product(*, db_product: Product = Depends(get_product_or_404)):
    """
    Get the product type by id
    """
    # Le righe commentate sotto, sostituite dalla nuova Depends
    # Nota: il parametro product_id a get_product_or_404 è preso dal path
    # p = session.get(Product, product_id)
    # if not p:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="Product type not found"
    #         )
    return db_product


# TODO: avoid DETAIL:  Key (type_id)=(2) is not present in table "producttype"
# se si passa producttype_id non esistente
@router.post("/", response_model=ProductRead)
async def create_product(*, session: Session = Depends(get_session),
                         product: ProductCreate) -> Any:
    """
    Create a new single product
    """
    db_product = Product.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product



@router.patch("/update/{product_id}", response_model=ProductRead)
async def update_product_by_id(*, session: Session = Depends(get_session),
                               product: ProductUpdate,
                               db_product: Product = Depends(get_product_or_404)):
    """
    Modify and existing product by id
    """
    # Le righe commentate sotto, sostituite dalla nuova Depends
    # Nota: il parametro product_id a get_product_or_404 è preso dal path
    # db_product = session.get(Product, product_id)
    # if not db_product:
    #     raise HTTPException(status_code=404, detail="Product not found")
    pr_data = product.dict(exclude_unset=True)
    for key, value in pr_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.patch("/update/by_name/{name}", response_model=ProductRead)
async def update_product_by_name(*, session: Session = Depends(get_session),
                                 product_name: str, product: ProductUpdate):
    """
    Modify an existing product by name
    """
    db_product = session.exec(
            select(Product).where(Product.name == product_name)
                 ).one()
    if not db_product:
        raise HTTPException(
            status_code=404, detail="Product not found, impossible to update"
        )
    pr_data = product.dict(exclude_unset=True)  # to use the nullable data
    for key, value in pr_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@router.delete("/{product_id}")
async def delete_product(*, session: Session = Depends(get_session),
                         product: Product = Depends(get_product_or_404)):
    """
    Delete and remove an existing product by id; it must be >= 1
    """
    # Le righe commentate sotto, sostituite dalla nuova Depends
    # Nota: il parametro product_id a get_product_or_404 è preso dal path
    # product = session.get(Product, product_id)
    # if not product:
    #     raise HTTPException(
    #         status_code=404, detail="Product not found, impossible to remove"
    #     )
    session.delete(product)
    session.commit()
    return {"ok": True}
