from pydantic import BaseModel, conint


class Vote(BaseModel):
    message_id: int
    dir: conint(le=1)
