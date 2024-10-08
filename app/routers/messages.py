from typing import Optional

from fastapi import Depends, HTTPException, APIRouter
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from sqlalchemy.orm import Session
from starlette import status

from app import models
from app.database import get_db
from .. import oauth2
from ..schemas import message as message_schemas

router = APIRouter(tags=["Messages"], prefix="/messages")


@router.get("/", response_model=list[message_schemas.Message])  # Get all messages
@cache(expire=100)
async def get_messages(
        db: Session = Depends(get_db),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = "",
        user: models.User = Depends(oauth2.get_current_user)
):
    messages = (
        db.query(models.Message)
        .filter(
            (models.Message.title + models.Message.content).contains(search.lower()),  # type: ignore
        )
        .limit(limit)
        .offset(skip)
        .all()
    )

    return messages


# Все сообщения, созданные пользователем
@router.get(
    "/by_me",
    response_model=list[message_schemas.Message]
)
@cache(expire=100)
async def get_messages_by_me(
        db: Session = Depends(get_db),
        user: models.User = Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = "",
):
    messages = (
        db.query(models.Message)
        .filter(
            (models.Message.title + models.Message.content).contains(search.lower()),  # type: ignore
            models.Message.creator_id == user.id,  # type: ignore
        )
        .limit(limit)
        .offset(skip)
        .all()
    )

    return messages


# Все сообщения, адресованные пользователю
@router.get('/for_me', response_model=list[message_schemas.Message])
@cache(expire=100)
async def get_messages_for_me(
        db: Session = Depends(get_db),
        user: models.User = Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = "",
):
    messages = (
        db.query(models.Message)
        .filter(
            (models.Message.title + models.Message.content).contains(search.lower()),  # type: ignore
            models.Message.receiver_id == user.id,  # type: ignore
        )
        .limit(limit)
        .offset(skip)
        .all()
    )

    return messages


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
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

    await FastAPICache.clear()
    return new_message


@router.get(
    "/{id}",
)  # Get one message
@cache(namespace="one_message")
def get_message(
        id: int,
        db: Session = Depends(get_db),
        user: models.User = Depends(oauth2.get_current_user)
):
    message = db.query(models.Message).filter(models.Message.id == id).first()
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message


@router.put("/{id}")  # Update message
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

    if message.creator_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to delete message with ID {id}",
        )

    message_query.update(updated_message.dict(), synchronize_session=False)

    db.commit()
    db.refresh(message)

    await FastAPICache.clear()

    return message


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

    await FastAPICache.clear()

    db.commit()
