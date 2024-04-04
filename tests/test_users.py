import pytest

from jose import jwt

from app.config import settings
from app.schemas import user as user_schemas, auth as auth_schemas
from .database import client, session


@pytest.fixture(scope="module") # Мега сомнительный тестик хз
def test_user(client):
    user_credentials = {'email': 'test123@gmail.com', 'password': 'test123', 'username': 'test123'}
    res = client.post('/users', json=user_credentials)

    new_user = res.json()

    new_user['password'] = user_credentials['password']
    new_user['email'] = user_credentials['email']

    assert res.status_code == 201

    return new_user


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
