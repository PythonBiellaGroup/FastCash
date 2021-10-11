from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from typing import List, Any
import datetime as dt
from app.src.common.utils import profiling_api

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
from app.src.common.security import get_current_user
from app.src.models.app_user import AppUser
from app.src.models.tag import Tag
from app.src.logger import logger


router = APIRouter()


async def get_product_or_404(
    *,
    session: Session = Depends(get_session),
    product_id: int = Path(..., ge=1),
    current_user: AppUser = Depends(get_current_user),
):
    start_time = dt.datetime.now()
    try:
        db_product = session.get(Product, product_id)
        if db_product:
            return {
                "db_product": db_product,
                "username": current_user.username,
                "start_time": start_time,
            }
        else:
            logger.error("Product not found")
            logger.exception("Product not found")
            raise HTTPException(status_code=404, detail="Product not found")
    except KeyError:
        logger.error("Product not found")
        logger.exception("KeyError: Product not found")
        raise HTTPException(status_code=400, detail="Product not found")


@router.get("/", response_model=List[ProductReadwithTypeAndTags])
async def read_all_products(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    current_user: AppUser = Depends(get_current_user),
) -> Any:
    """
    Retrieve all products
    """
    start_time = dt.datetime.now()
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    profiling_api("Product:get:all", start_time, current_user.username)
    return products


@router.get("/{product_id}", response_model=ProductReadwithTypeAndTags)
async def read_product(
    *, product_id: int, db_product: Product = Depends(get_product_or_404)
):
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
    profiling_api(
        f"Product:read:by_id:{product_id}",
        db_product["start_time"],
        db_product["username"],
    )
    return db_product["db_product"]


@router.post("/", response_model=ProductRead)
async def create_product(
    *,
    session: Session = Depends(get_session),
    product: ProductCreate,
    current_user: AppUser = Depends(get_current_user),
) -> Any:
    """
    Create a new single product
    """
    start_time = dt.datetime.now()
    # Controllo esistenza product type
    _ = await get_producttype_or_404(producttype_id=product.type_id, session=session)
    # Controllo integrità o altri errori
    try:
        db_product = Product.from_orm(product)
        session.add(db_product)
        session.commit()
        profiling_api("Product:insert:single", start_time, current_user.username)
    except IntegrityError:
        logger.error("Impossible to create product with same name")
        logger.exception("Integrity Error: Impossible to create product with same name")
        raise HTTPException(
            status_code=404, detail="Impossible to create product with same name"
        )
    session.refresh(db_product)
    return db_product


@router.patch("/update/{product_id}", response_model=ProductRead)
async def update_product_by_id(
    *,
    product_id: int,
    session: Session = Depends(get_session),
    product: ProductUpdate,
    db_product: Product = Depends(get_product_or_404),
):
    """
    Modify and existing product by id
    """
    # Le righe commentate sotto, sostituite dalla nuova Depends
    # Nota: il parametro product_id a get_product_or_404 è preso dal path
    # db_product = session.get(Product, product_id)
    # if not db_product:
    #     raise HTTPException(status_code=404, detail="Product not found")
    existing_product = db_product["db_product"]
    pr_data = product.dict(exclude_unset=True)

    for key, value in pr_data.items():
        setattr(existing_product, key, value)

    session.add(existing_product)
    session.commit()
    session.refresh(existing_product)

    profiling_api(
        f"Product:update:by_id:{product_id}",
        db_product["start_time"],
        db_product["username"],
    )
    return existing_product


@router.patch("/update/by_name/{product_name}", response_model=ProductRead)
async def update_product_by_name(
    *,
    session: Session = Depends(get_session),
    product_name: str,
    product: ProductUpdate,
    current_user: AppUser = Depends(get_current_user),
):
    """
    Modify an existing product by name
    """
    start_time = dt.datetime.now()
    db_product = session.exec(select(Product).where(Product.name == product_name)).one()
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
    profiling_api(
        f"Product:update:by_name:{product_name}",
        start_time,
        current_user.username,
    )
    return db_product


@router.patch(
    "/update/{product_id}/add_tag_by_id/{tag_id}",
    response_model=ProductReadwithTypeAndTags,
)
async def update_product_add_tag_by_id(
    *,
    product_id: int,
    session: Session = Depends(get_session),
    db_product: Product = Depends(get_product_or_404),
    db_tag: Tag = Depends(get_tag_or_404),
):
    """
    Add tag to product
    """
    existing_product = db_product["db_product"]
    existing_tag = db_tag["db_tag"]

    existing_product.tags.append(existing_tag)
    session.add(existing_product)
    session.commit()
    session.refresh(existing_product)

    profiling_api(
        f"Product:update:add_tag:by_id:{product_id}",
        db_product["start_time"],
        db_product["username"],
    )
    return existing_product


@router.patch(
    "/update/{product_id}/add_tag_by_name/{tag_name}",
    response_model=ProductReadwithTypeAndTags,
)
async def update_product_add_tag_by_name(
    *,
    product_id: int,
    session: Session = Depends(get_session),
    db_product: Product = Depends(get_product_or_404),
    db_tag: Tag = Depends(get_tag_by_name_or_404),
):
    """
    Add tag to product
    """
    existing_product = db_product["db_product"]
    existing_tag = db_tag["db_tag"]

    existing_product.tags.append(existing_tag)
    session.add(existing_product)
    session.commit()
    session.refresh(existing_product)

    profiling_api(
        f"Product:update:add_tag:by_name:{product_id}",
        db_product["start_time"],
        db_product["username"],
    )
    return existing_product


@router.patch(
    "/update/{product_id}/remove_tag_by_id/{tag_id}",
    response_model=ProductReadwithTypeAndTags,
)
async def update_product_remove_tag_by_id(
    *,
    product_id: int,
    session: Session = Depends(get_session),
    db_product: Product = Depends(get_product_or_404),
    db_tag: Tag = Depends(get_tag_or_404),
):
    """
    Remove tag from product
    """
    existing_product = db_product["db_product"]
    existing_tag = db_tag["db_tag"]
    try:
        existing_product.tags.remove(existing_tag)
        session.add(existing_product)
        session.commit()
        session.refresh(existing_product)

        profiling_api(
            f"Product:update:remove_tag:by_id:{product_id}",
            db_product["start_time"],
            db_product["username"],
        )
    except Exception as message:
        logger.error(message)
        logger.exception(message)
        raise HTTPException(
            status_code=404,
            detail="Impossible to remove the tag: product or tag not existing",
        )
    return existing_product


@router.patch(
    "/update/{product_id}/remove_tag_by_name/{tag_name}",
    response_model=ProductReadwithTypeAndTags,
)
async def update_product_remove_tag_by_name(
    *,
    product_id: int,
    session: Session = Depends(get_session),
    db_product: Product = Depends(get_product_or_404),
    db_tag: Tag = Depends(get_tag_by_name_or_404),
):
    """
    Remove tag from product
    """
    existing_db_product = db_product["db_product"]
    existing_db_tag = db_tag["db_tag"]

    db_product.tags.remove(existing_db_tag)
    session.add(existing_db_product)
    session.commit()
    session.refresh(existing_db_product)

    profiling_api(
        f"Product:update:remove_tag:by_name:{product_id}",
        db_product["start_time"],
        db_product["username"],
    )
    return db_product


@router.delete("/{product_id}")
async def delete_product(
    *,
    product_id: int,
    session: Session = Depends(get_session),
    db_product: Product = Depends(get_product_or_404),
):
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
    existing_db_product = db_product["db_product"]
    session.delete(existing_db_product)
    session.commit()
    profiling_api(
        f"Product:update:add_tag:by_id:{product_id}",
        db_product["start_time"],
        db_product["username"],
    )
    return {"ok": True}
