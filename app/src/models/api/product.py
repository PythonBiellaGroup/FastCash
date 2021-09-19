from typing import TYPE_CHECKING, Optional
from app.src.schemas.entities import ProductBase


if TYPE_CHECKING:
    from app.src.models.api.product_type import ProductTypeRead


class ProductRead(ProductBase):
    id: int
    name: str
    description: str
    price: float
    available: bool
    type_id: Optional[int] = None


class ProductCreate(ProductBase):
    name: str
    description: str
    price: float
    available: bool
    type_id: Optional[int] = None


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None
    type_id: Optional[int] = None


class ProductDelete(ProductBase):
    pass


class ProductReadwithType(ProductRead):
    product_type: Optional["ProductTypeRead"] = None
