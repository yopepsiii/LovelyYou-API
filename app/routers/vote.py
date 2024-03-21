from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..schemas import vote as vote_schemas
from .. import models, oauth2, database

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def like(
    vote: vote_schemas.Vote,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(oauth2.get_current_user),
):
    message = db.query(models.Message).filter(models.Message.id == vote.message_id).first()  #type: ignore
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Message {vote.message_id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.message_id == vote.message_id, models.Vote.user_id == user.id)  #type: ignore

    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user.id} already liked message {vote.message_id}")
        new_vote = models.Vote(message_id=vote.message_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "liked successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"like from user {user.id} for message {vote.message_id} was not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "like removed successfully"}


