from fastapi import APIRouter

from app.src.api.endpoints import product, tags, product_type, app_user, login

api_router = APIRouter()
api_router.include_router(product.router, prefix="/products", tags=["product"])
api_router.include_router(tags.router, prefix="/tags", tags=["tag"])
api_router.include_router(
    product_type.router, prefix="/product_type", tags=["product_type"]
)
api_router.include_router(app_user.router, prefix="/user", tags=["user"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
