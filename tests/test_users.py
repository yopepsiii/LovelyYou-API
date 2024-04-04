import pytest
from jose import jwt

from app.config import settings
from app.schemas import user as user_schemas, auth as auth_schemas


def test_root(client):
    res = client.get("/")
    print(res.json())


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "hello123@gmail.com", "password": "password123", "username": "bebra"})

    new_user = user_schemas.UserOut(**res.json())
    assert new_user.username == "bebra"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    token_res = auth_schemas.Token(**res.json())
    payload = jwt.decode(token=token_res.access_token, algorithms=settings.algorithm, key=settings.secret_key)
    id = payload.get('id')
    assert res.status_code == 200
    assert token_res.token_type == 'bearer'


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'test123', 403),
    ('test123@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'test123', 422),
    ('test123@gmail.com', None, 422)
])
def test_incorrect_login_user(client, test_user, email, password, status_code):
    res = client.post('/login', data={"username": email, "password": password})
    assert res.status_code == status_code
