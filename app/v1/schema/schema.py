from uuid import UUID

from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    city: str
    username: str
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str