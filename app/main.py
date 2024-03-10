

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from sqlalchemy.orm import Session
from starlette import status

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class MessageScheme(BaseModel):
    title: str
    content: str


my_messages = [{"title": "Любитель бебр", "content": "О да, я очень люблю капибар", "id": 1},
               {"title": "Очень круто круто очень", "content": "Ну как бы да, прям вообще зашибись но блин", "id": 2}]


@app.get("/sqltest")
async def bd_test():

    return {"status": "conection was successful"}


async def find_message_by_id(message_id: int):
    for message in my_messages:
        if message["id"] == message_id:
            return message


async def find_index_of_message(message_id: int):
    for i, message in enumerate(my_messages):
        if message["id"] == message_id:
            return i


@app.get("/")
async def root():
    return {"message": "Hi!1!"}


@app.get("/messages")  # Get all messages
async def get_messages(db: Session = Depends(get_db)):
    messages = db.query(models.Message).all()
    return {"messages": messages}


@app.post("/messages", status_code=status.HTTP_201_CREATED)  # Create a message
async def create_message(message: MessageScheme, db: Session = Depends(get_db)):
    new_message = models.Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return {"message": new_message}


@app.get("/messages/{id}")  # Get one message
async def get_message(id: int, db: Session = Depends(get_db)):
    message = db.query(models.Message).filter(models.Message.id == id).first()  # type: ignore
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message {id} was not found")
    return message


@app.put("/messages/{id}")  # Update message
async def update_message(id: int, update_message: MessageScheme):
    index = await find_index_of_message(id)
    print(index)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message to update with ID: {id} was not found")
    update_message_dict = update_message.dict()
    update_message_dict['id'] = id
    my_messages[index] = update_message_dict
    return {"message": update_message_dict}


@app.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(id: int):
    index = await find_index_of_message(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message {id} doesn't exist")
    my_messages.pop(index)
    return {"result": f"message {id} was deleted"}
