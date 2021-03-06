from pydantic import BaseModel


class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str

class User(UserBase):
    id: int
    name: str

    class Config:
        orm_mode = True

