from pydantic import BaseModel


class MessageBase(BaseModel):
    title: str
    content: str


class CreateMessage(MessageBase):
    pass


class UpdateMessage(MessageBase):
    pass
