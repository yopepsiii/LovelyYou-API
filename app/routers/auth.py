from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .. import schemas, models, utils
from ..database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()  # type: ignore
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this credentials was not founded")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this credentials was not founded")

    # create a token
    # return token
    return {"access_token": "token"}
