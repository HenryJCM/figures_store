from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

class SaleDetailBase(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: float

class SaleDetailOut(SaleDetailBase):
    id: UUID

class SaleBase(BaseModel):
    client_id: UUID
    date: datetime
    total: float

class SaleOut(SaleBase):
    id: UUID
    sale_details: List[SaleDetailOut] = []

    class Config:
        from_attributes = True