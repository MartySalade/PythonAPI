from pydantic import BaseModel

class OrderBase(BaseModel):
    name: str
    price: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

#-----------------------------#

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    id: int

class User(UserBase):
    id: int
    orders: list[Order] = []

    class Config:
        orm_mode = True

