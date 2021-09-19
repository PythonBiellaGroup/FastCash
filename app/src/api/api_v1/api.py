from fastapi import APIRouter

from app.src.api.api_v1.endpoints import product

api_router = APIRouter()
api_router.include_router(product.router, prefix="/products", tags=["product"])
# api_router.include_router(tags.router, prefix="/tags", tags=["tag"])
# api_router.include_router(product_type.router, prefix="/product_type", tags=["product_type"])
