from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: str
    stock: int
    brand_id: UUID

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class ProductBrandUpdate(BaseModel):
    brand_id: UUID

class ProductResponse(ProductBase):
    id: UUID
    brand_id: UUID

    class Config:
        orm_mode = True