from uuid import UUID
from pydantic import BaseModel

class BrandBase(BaseModel):
    name: str

class BrandCreate(BrandBase):
    pass

class BrandResponse(BrandBase):
    id: UUID

    class Config:
        from_attributes = True
