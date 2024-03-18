from datetime import datetime
from pydantic import BaseModel


class MessageBase(BaseModel):
    title: str
    content: str
    creator_id: int
    receiver_id: int


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

