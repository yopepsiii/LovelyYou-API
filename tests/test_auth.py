from jose import jwt

from app.config import settings
from app.schemas import auth as auth_schemas
from .database import client


def test_login_user(client):
    res = client.post(
        "/login", data={"username": "hello123@gmail.com", "password": "password123"})
    token_res = auth_schemas.Token(**res.json())
    payload = jwt.decode(token=token_res["access_token"], algorithms=settings.algorithm, key=settings.secret_key)
    id = payload['id']
    assert res.status_code == 200
    assert token_res.token_type == 'bearer'
