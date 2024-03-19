from datetime import datetime
from pydantic import BaseModel
from ..schemas import user as user_schemas


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
    creator: user_schemas.UserOut
    receiver: user_schemas.UserOut

    class Config:
        from_attributes = True
