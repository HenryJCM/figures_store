from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: str
    stock: int
    brand_id: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: UUID

    class Config:
        orm_mode = True