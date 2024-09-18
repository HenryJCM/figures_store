from uuid import UUID

from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    email: str
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str