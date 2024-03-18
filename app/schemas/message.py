from datetime import datetime
from pydantic import BaseModel


class MessageBase(BaseModel):
    title: str
    content: str


class MessageCreate(MessageBase):
    receiver_id: int


class MessageUpdate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    created_at: datetime
    creator_id: int
    receiver_id: int

    class Config:
        from_attributes = True
