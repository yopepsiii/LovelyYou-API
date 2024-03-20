from typing import Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app import models
from app.database import get_db
from .. import oauth2
from ..schemas import message as message_schemas

router = APIRouter(tags=["messages"])


@router.get(
    "/messages", response_model=list[message_schemas.Message]
)  # Get all messages
async def get_messages(
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    print(search)
    messages = db.query(models.Message).filter(models.Message.title.contains(search)).limit(limit).offset(skip).all()  # type: ignore
    return messages


@router.post(
    "/messages",
    status_code=status.HTTP_201_CREATED,
    response_model=message_schemas.Message,
)  # Create a message
async def create_message(
    message: message_schemas.MessageCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    new_message = models.Message(creator_id=user.id, **message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


@router.get(
    "/messages/{id}",
    response_model=message_schemas.Message,
)  # Get one message
async def get_message(
    id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    message = db.query(models.Message).filter(models.Message.id == id).first()  # type: ignore
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"message {id} was not found"
        )
    return message


@router.put("/messages/{id}")  # Update message
async def update_message(
    id: int,
    updated_message: message_schemas.MessageUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    message_query = db.query(models.Message).filter(models.Message.id == id)  # type: ignore
    message = message_query.first()

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"message {id} was not found"
        )

    message_query.update(updated_message.dict(), synchronize_session=False)

    db.commit()
    db.refresh(message)

    return message


@router.delete("/messages/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    message_query = db.query(models.Message).filter(models.Message.id == id)  # type: ignore
    message = message_query.first()
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"message with ID {id} was not find",
        )

    if message.creator_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to delete message with ID {id}",
        )
    message_query.delete(synchronize_session=False)

    db.commit()