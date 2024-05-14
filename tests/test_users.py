import pytest
from jose import jwt

from app.config import settings
from app.schemas import user as user_schemas, auth as auth_schemas


def test_root(client):
    res = client.get("/")
    print(res.json())


def test_create_user(client):
    res = client.post(
        "/users",
        json={
            "email": "hello123@gmail.com",
            "password": "password123",
            "username": "bebra",
        },
    )

    new_user = user_schemas.UserOut(**res.json())
    assert new_user.username == "bebra"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    token_res = auth_schemas.Token(**res.json())
    payload = jwt.decode(
        token=token_res.access_token,
        algorithms=settings.algorithm,
        key=settings.secret_key,
    )
    id = payload.get("id")
    assert res.status_code == 200
    assert token_res.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "test123", 403),
        ("test123@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "test123", 422),
        ("test123@gmail.com", None, 422),
    ],
)
def test_incorrect_login_user(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code


@pytest.mark.parametrize(
    "email, username, password, status_code",
    [
        ("test345@gmail.com", "new_bebra", "new_test123", 200),
        (None, "new_bebra", "new_test123", 422),
        ("test345@gmail.com", None, "new_test123", 422),
        ("test345@gmail.com", "new_bebra", None, 422),
        (None, None, "new_test123", 422),
        (None, "new_bebra", None, 422),
        ("test345@gmail.com", None, None, 422),
        (None, None, None, 422),
    ],
)
def test_update_user(
    authorized_client, test_user, email, username, password, status_code
):
    data = {"email": email, "password": password, "username": username}
    res = authorized_client.put(f'/users/{test_user["id"]}', json=data)
    print(res.json())
    assert res.status_code == status_code

    if res.status_code != 422:
        updated_user = user_schemas.UserUpdate(**res.json())

        print(updated_user)

        assert updated_user.email == data["email"]
        assert updated_user.password == data["password"]
        assert updated_user.username == data["username"]


def test_update_unexisting_user(authorized_client):
    data = {"email": "email@gmail.com", "password": "password", "username": "username"}
    res = authorized_client.put(f"/users/9999999", json=data)
    assert res.status_code == 404


def test_update_unauthorized_user(client, test_user):
    data = {"email": "email@gmail.com", "password": "password", "username": "username"}
    res = client.put(f'/users/{test_user["id"]}', json=data)
    assert res.status_code == 401


def test_update_another_user(authorized_client, test_user, test_user2):
    data = {"email": "email@gmail.com", "password": "password", "username": "username"}
    res = authorized_client.put(f'/users/{test_user2["id"]}', json=data)
    assert res.status_code == 403
