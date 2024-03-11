from fastapi import FastAPI, HTTPException, Depends


from sqlalchemy.orm import Session
from starlette import status

from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/sqltest")
async def bd_test():
    return {"status": "conection was successful"}


@app.get("/")
async def root():
    return {"message": "Hi!1!"}


@app.get("/messages", response_model=list[schemas.Message])  # Get all messages
async def get_messages(db: Session = Depends(get_db)):
    messages = db.query(models.Message).all()
    return messages


@app.post("/messages", status_code=status.HTTP_201_CREATED, response_model=schemas.Message)  # Create a message
async def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    new_message = models.Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


@app.get("/messages/{id}", response_model=schemas.Message)  # Get one message
async def get_message(id: int, db: Session = Depends(get_db)):
    message = db.query(models.Message).filter(models.Message.id == id).first()  # type: ignore
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message {id} was not found")
    return message


@app.put("/messages/{id}")  # Update message
async def update_message(id: int, updated_message: schemas.MessageUpdate, db: Session = Depends(get_db)):
    message_query = db.query(models.Message).filter(models.Message.id == id)  # type: ignore
    message = message_query.first()

    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message {id} was not found")

    message_query.update(updated_message.dict())

    db.commit()
    db.refresh(message)

    return message


@app.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT, )
async def delete_message(id: int, db: Session = Depends(get_db)):
    message_to_delete = db.query(models.Message).filter(models.Message.id == id)  # type: ignore

    if message_to_delete.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message with ID {id} was not find")
    message_to_delete.delete(synchronize_session=False)
    db.commit()


@app.get("/users", response_model=list[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    messages = db.query(models.User).all()
    return messages


@app.get("/users/{id}", response_model=schemas.UserOut)
async def get_users(id: int, db: Session = Depends(get_db)):
    message = db.query(models.User).filter(models.User.id == id).first()  # type: ignore
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message with ID {id} not found")
    return message


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)  # Create a message
async def create_message(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# 6:26:24
