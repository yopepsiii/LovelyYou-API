from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    print(res.json())


def test_create_user():
    res = client.post("/users/", json={"username": "bebra", "email": "bebra228@gmail.com", "password": "AloHuis"})
    print(res.json())
    assert res.status_code == 201
