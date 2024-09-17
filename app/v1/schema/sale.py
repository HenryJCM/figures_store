import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

class SaleDetailBase(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: float
    date_added: str

class SaleDetailOut(SaleDetailBase):
    id: UUID

class SaleBase(BaseModel):
    user_id: UUID
    date: str
    total: float

class SaleOut(SaleBase):
    id: UUID
    sale_details: List[SaleDetailOut] = []

    class Config:
        from_attributes = True