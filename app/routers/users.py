from fastapi import Depends, HTTPException, APIRouter
from fastapi_cache import FastAPICache
from sqlalchemy.orm import Session
from starlette import status

from .. import models, utils, oauth2
from ..schemas import user as user_schemas
from ..schemas import auth as auth_schemas
from ..database import get_db

router = APIRouter(tags=["Users"], prefix="/users")


@router.get("/", response_model=list[user_schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=user_schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()  # type: ignore
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with ID {id} not found"
        )
    return user


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=auth_schemas.Token
)  # Create a user
async def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    await FastAPICache.clear()

    access_token = await oauth2.create_access_token(data={"user_id": new_user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/{id}", response_model=user_schemas.UserUpdate)
async def update_user(
    id: int,
    updated_user: user_schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_query = db.query(models.User).filter(models.User.id == id)  # type: ignore
    user = user_query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} is not exists",
        )
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to update user with ID {id}",
        )

    user_query.update(updated_user.dict(), synchronize_session=False)

    db.commit()
    db.refresh(user)

    await FastAPICache.clear()

    return user
