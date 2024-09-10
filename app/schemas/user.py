from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    username: str
    id: int


class UserFullInfo(UserOut):
    email: EmailStr
    created_at: datetime
