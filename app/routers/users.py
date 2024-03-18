from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from .. import models, utils
from ..oauth2 import create_access_token
from ..schemas import user as user_schemas
from ..database import get_db

router = APIRouter(tags=["Users"], prefix="/users")


@router.get("/", response_model=list[user_schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=user_schemas.UserOut)
async def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()  # type: ignore
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with ID {id} not found"
        )
    return user


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserOut
)  # Create a message
async def create_message(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
