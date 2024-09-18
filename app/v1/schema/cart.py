from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

class CartBase(BaseModel):
    product_id: UUID

class CartUpdate(BaseModel):
    quantity: int

class CartOut(CartBase):
    id: UUID
    client_id: UUID
    date_added: datetime
    quantity: int

    class Config:
        from_attributes = True

class CartListBase(BaseModel):
    items: List[CartOut]