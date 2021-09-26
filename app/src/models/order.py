from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class OrderBase(SQLModel):
    total_price: float
    discount: float
    order_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note: Optional[str]
