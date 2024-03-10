from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy.orm import Session
from starlette import status

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/sqltest")
async def bd_test():
    return {"status": "conection was successful"}

@app.get("/")
async def root():
    return {"message": "Hi!1!"}

@app.get("/messages")  # Get all messages
async def get_messages(db: Session = Depends(get_db)):
    messages = db.query(models.Message).all()
    return {"messages": messages}


@app.post("/messages", status_code=status.HTTP_201_CREATED)  # Create a message
async def create_message(message: schemas.CreateMessage, db: Session = Depends(get_db)):
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
    return {"message": message}


@app.put("/messages/{id}")  # Update message
async def update_message(id: int, update_message: schemas.UpdateMessage, db: Session = Depends(get_db)):
    message_query = db.query(models.Message).filter(models.Message.id == id)  # type: ignore
    message = message_query.first()

    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message {id} was not found")

    message_query.update(update_message.dict())

    db.commit()
    db.refresh(message)

    return {"updated_message": message}


@app.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT, )
async def delete_message(id: int, db: Session = Depends(get_db)):
    message_to_delete = db.query(models.Message).filter(models.Message.id == id)  # type: ignore

    if message_to_delete.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message with ID {id} was not find")
    message_to_delete.delete(synchronize_session=False)
    db.commit()

# 5:38:36