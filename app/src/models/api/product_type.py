from typing import TYPE_CHECKING, Optional
from app.src.schemas.entities import ProductTypeBase


if TYPE_CHECKING:
    from app.src.models.api.product import ProductRead


class ProductTypeRead(ProductTypeBase):
    id: int
    name: str
    description: str
    price: float
    available: bool


class ProductTypeReadwithProduct(ProductTypeBase):
    product_type: Optional["ProductRead"] = None
