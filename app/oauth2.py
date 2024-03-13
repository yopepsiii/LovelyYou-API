from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = '59gkrEkhgk5078gjfnbvfkg84mfdFKGFGK20IF'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
