from jose import jwt

from app.config import settings
from app.schemas import user as user_schemas, auth as auth_schemas
from .database import client


def test_root(client):
    res = client.get("/")
    print(res.json())


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123", "username": "bebra"})

    new_user = user_schemas.UserOut(**res.json())
    assert new_user.username == "bebra"
    assert res.status_code == 201


