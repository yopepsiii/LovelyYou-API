from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, models
from app.database import get_db

router = APIRouter(tags=["messages"])


@router.get("/messages", response_model=list[schemas.Message])  # Get all messages
async def get_messages(db: Session = Depends(get_db)):
    messages = db.query(models.Message).all()
    return messages


@router.post("/messages", status_code=status.HTTP_201_CREATED, response_model=schemas.Message)  # Create a message
async def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    new_message = models.Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


@router.get("/messages/{id}", response_model=schemas.Message)  # Get one message
async def get_message(id: int, db: Session = Depends(get_db)):
    message = db.query(models.Message).filter(models.Message.id == id).first()  # type: ignore
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message {id} was not found")
    return message


@router.put("/messages/{id}")  # Update message
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


@router.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT, )
async def delete_message(id: int, db: Session = Depends(get_db)):
    message_to_delete = db.query(models.Message).filter(models.Message.id == id)  # type: ignore

    if message_to_delete.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message with ID {id} was not find")
    message_to_delete.delete(synchronize_session=False)
    db.commit()
