from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    mobile: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    split_method: str
    participants: List[int]

class ExpenseSplit(BaseModel):
    user_id: int
    amount: float

    class Config:
        orm_mode = True

class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: float
    created_by: int
    splits: List[ExpenseSplit]

    class Config:
        orm_mode = True
        from_attributes = True