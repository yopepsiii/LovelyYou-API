from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class MessageBase(BaseModel):
    title: str
    content: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


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
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
