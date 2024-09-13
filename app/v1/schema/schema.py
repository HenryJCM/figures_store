from uuid import UUID

from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    city: str
    username: str
    hashed_password: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: UUID

    class Config:
        orm_mode = True