from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

# if TYPE_CHECKING:
#    from app.src.models.db.order import Order


class AppUserBase(SQLModel):
    username: str
    name: Optional[str]
    surname: Optional[str]
    birth_date: Optional[date]
    email: str
    password: str
    isAdmin: bool = False


class AppUser(AppUserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class AppUserCreate(AppUserBase):
    pass


class AppUserRead(AppUserBase):
    id: int


# Nel modello update tutti gli attributi devono essere opzionali
class AppUserUpdate(AppUserBase):
    name: Optional[str] = None
    surname: Optional[str] = None
    birth_date: Optional[date] = None
    username: Optional[str] = None
    email: str
    password: str
    isAdmin: Optional[bool] = None
