from fastapi import APIRouter

from live.src.api.endpoints import product

api_router = APIRouter()

api_router.include_router(product.router, prefix="/products", tags=['product'])
#api_router.include_router(..., prefix="/tags", tags=['tags'])
#api_router.include_router(..., prefix="/product-type", tags=['product-type'])