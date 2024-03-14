from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from .. import models, utils, oauth2
from ..database import get_db
from ..schemas import auth as auth_schemas

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=auth_schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()  # type: ignore
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    acces_token = await oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": acces_token, "token_type": "bearer"}
