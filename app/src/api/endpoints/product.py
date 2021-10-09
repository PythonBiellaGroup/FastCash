import logging
from app.src.models.tag import Tag
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List, Any

from app.src.logger import logger
from app.src.models.product import (
    Product,
    ProductRead,
    ProductCreate,
    ProductUpdate,
    ProductReadwithTypeAndTags,
)
from app.src.db.engine import get_session
from app.src.api.endpoints.product_type import get_producttype_or_404
from app.src.api.endpoints.tags import get_tag_or_404, get_tag_by_name_or_404


router = APIRouter()


async def get_product_or_404(
    *, session: AsyncSession = Depends(get_session), product_id: int = Path(..., ge=1)
):
    try:
        result = await session.execute(select(Product).where(Product.id == product_id))
        db_product = result.scalars().first()        
        if db_product:
            logger.info(f"Trovato product: {db_product}")
            return db_product
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except KeyError:
        raise HTTPException(status_code=400, detail="Product not found")


async def get_product_by_name_or_404(
    *, session: AsyncSession = Depends(get_session), product_name: str
):
    try:
        result = await session.execute(select(Product).where(Product.name == product_name))
        db_product = result.scalars().first()        
        if db_product:
            logger.info(f"Trovato (per nome): {db_product}")
            return db_product
        else:
            raise HTTPException(status_code=404, detail="Product by name not found")
    except KeyError:
        raise HTTPException(status_code=400, detail="Product by name not found")



# Funziona solo con response model ProductRead
# @router.get("/", response_model=List[ProductReadwithTypeAndTags])
@router.get("/", response_model=List[ProductRead])
async def read_all_products(
    session: AsyncSession = Depends(get_session)
) -> Any:
    """
    Retrieve all products
    """
    # products = session.exec(select(Product).offset(offset).limit(limit)).all()
    result = await session.execute(select(Product))
    products = result.scalars().all()
    return products


# Funziona solo con response model ProductRead
# @router.get("/{product_id}", response_model=ProductReadwithTypeAndTags)
@router.get("/{product_id}", response_model=ProductRead)
async def read_product(*, db_product: Product = Depends(get_product_or_404)):
    """
    Get the product type by id
    """
    return db_product


@router.post("/", response_model=ProductRead)
async def create_product(
    *, session: AsyncSession = Depends(get_session), product: ProductCreate
) -> Any:
    """
    Create a new single product
    """
    # Controllo esistenza product type
    _ = await get_producttype_or_404(producttype_id=product.type_id, session=session)
    # Controllo integrità o altri errori
    try:
        db_product = Product.from_orm(product)
        session.add(db_product)
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=404, detail="Impossible to create product with same name"
        )
    await session.flush(db_product)
    return db_product


@router.patch("/update/{product_id}", response_model=ProductRead)
async def update_product_by_id(
    *,
    session: AsyncSession = Depends(get_session),
    product: ProductUpdate,
    db_product: Product = Depends(get_product_or_404)
):
    """
    Modify and existing product by id
    """
    pr_data = product.dict(exclude_unset=True)
    for key, value in pr_data.items():
        setattr(db_product, key, value)
    logger.info(f"Modificato: {db_product}")
    session.add(db_product)
    await session.commit()
    await session.flush(db_product)
    return db_product


@router.patch("/update/by_name/{name}", response_model=ProductRead)
async def update_product_by_name(
    *,
    session: AsyncSession = Depends(get_session),
    product_name: str,
    product: ProductUpdate
):
    """
    Modify an existing product by name
    """
    result = await session.execute(select(Product).where(Product.name == product_name))
    db_product = result.scalars().first()        
    if not db_product:
        raise HTTPException(
            status_code=404, detail="Product not found, impossible to update"
        )
    pr_data = product.dict(exclude_unset=True)  # to use the nullable data
    for key, value in pr_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    await session.commit()
    await session.flush(db_product)
    return db_product


# NON FUNZIONA - Relazione many-to-many
# "/update/{product_id}/add_tag_by_id/{tag_id}", response_model=ProductReadwithTypeAndTags
@router.patch(
    "/update/{product_id}/add_tag_by_id/{tag_id}", response_model=ProductRead
)
async def update_product_add_tag_by_id(
    *,
    session: AsyncSession = Depends(get_session),
    db_product: Product = Depends(get_product_or_404),
    db_tag: Tag = Depends(get_tag_or_404)
):
    """
    Add tag to product
    """
    if db_tag:
        logger.info(f"(update_product_add_tag_by_id) Trovato tag: {db_tag}")
    else:
        logger.info(f"(update_product_add_tag_by_id) NON Trovato tag...")
    # db_product.tags.append(db_tag)    
    logger.info(f"(update_product_add_tag_by_id) db_product {db_product}")
    tags = await db_product.tags
    logger.info(f"(update_product_add_tag_by_id) tags di db_product {db_product.tags}")
    # La session di SQLAlchemy gestisce in altro modo le relazioni
    # db_product.tags ritorna eccezione sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called
    db_product.tags.append(db_tag)
    session.add(db_product)
    await session.commit()
    await session.flush(db_product)
    return db_product


# NON FUNZIONA - Relazione many-to-many
@router.patch(
    "/update/{product_id}/add_tag_by_name/{tag_name}", response_model=ProductReadwithTypeAndTags
)
async def update_product_add_tag_by_name(
    *,
    session: AsyncSession = Depends(get_session),
    db_product: Product = Depends(get_product_or_404),
    db_tag: Tag = Depends(get_tag_by_name_or_404)
):
    """
    Add tag to product
    """
    db_product.tags.append(db_tag)
    session.add(db_product)
    await session.commit()
    await session.flush(db_product)
    return db_product


@router.patch(
    "/update/{product_id}/remove_tag_by_id/{tag_id}",
    response_model=ProductReadwithTypeAndTags,
)
async def update_product_remove_tag_by_id(
    *,
    session: AsyncSession = Depends(get_session),
    db_product: Product = Depends(get_product_or_404),
    db_tag: Tag = Depends(get_tag_or_404)
):
    """
    Remove tag from product
    """
    db_product.tags.remove(db_tag)
    session.add(db_product)
    await session.commit()
    await session.flush(db_product)
    return db_product


# NON FUNZIONA - Relazione many-to-many
@router.patch(
    "/update/{product_id}/remove_tag_by_name/{tag_name}",
    response_model=ProductReadwithTypeAndTags,
)
async def update_product_remove_tag_by_name(
    *,
    session: AsyncSession = Depends(get_session),
    db_product: Product = Depends(get_product_or_404),
    db_tag: Tag = Depends(get_tag_by_name_or_404)
):
    """
    Remove tag from product
    """
    db_product.tags.remove(db_tag)
    session.add(db_product)
    await session.commit()
    await session.flush(db_product)
    return db_product


@router.delete("/{product_id}")
async def delete_product(
    *,
    session: AsyncSession = Depends(get_session),
    product: Product = Depends(get_product_or_404)
):
    """
    Delete and remove an existing product by id; it must be >= 1
    """
    await session.delete(product)
    await session.commit()
    await session.flush(product)    
    return {"ok": True}
