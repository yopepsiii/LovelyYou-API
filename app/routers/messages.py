from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from ..schemas import message as message_schemas
from app.database import get_db
from .. import oauth2, models

router = APIRouter(tags=["Messages"], prefix="/messages")


@router.get("/", response_model=list[message_schemas.Message])  # Get all messages
async def get_messages(db: Session = Depends(get_db)):
    messages = db.query(models.Message).all()
    return messages


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=message_schemas.Message)  # Create a message
async def create_message(message: message_schemas.MessageCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    new_message = models.Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


@router.get("/{id}", response_model=message_schemas.Message, )  # Get one message
async def get_message(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    message = db.query(models.Message).filter(models.Message.id == id).first()  # type: ignore
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"message {id} was not found")
    return message


@router.put("/{id}")  # Update message
async def update_message(id: int, updated_message: message_schemas.MessageUpdate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    message_query = db.query(models.Message).filter(models.Message.id == id)  # type: ignore
    message = message_query.first()

    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message {id} was not found")

    message_query.update(updated_message.dict())

    db.commit()
    db.refresh(message)

    return message


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, )
async def delete_message(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    message_to_delete = db.query(models.Message).filter(models.Message.id == id)  # type: ignore

    if message_to_delete.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"message with ID {id} was not find")
    message_to_delete.delete(synchronize_session=False)
    db.commit()
