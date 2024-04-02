from app.schemas import user as user_schemas
from .database import client, session


def test_root(client):
    res = client.get("/")
    print(res.json())


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123", "username": "bebra"})

    new_user = user_schemas.UserOut(username=res.json["username"])
    assert new_user.username == "bebra"
    assert res.status_code == 201
