from sqlmodel import SQLModel
from typing import Optional


class MenuBase(SQLModel):
    name: str
    description: Optional[str]
    price: str
    available: bool = True
