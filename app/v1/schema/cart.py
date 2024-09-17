from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

class CartBase(BaseModel):
    product_id: UUID

class CartUpdate(CartBase):
    quantity: int

class CartOut(CartUpdate):
    id: UUID
    user_id: UUID
    date_added: datetime

    class Config:
        from_attributes = True

class CartListBase(BaseModel):
    items: List[CartOut]