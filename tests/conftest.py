from functools import wraps

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.config import settings
from app.database import get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}-test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    from app.main import app
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_credentials = {
        "email": "test123@gmail.com",
        "password": "test123",
        "username": "bebrta",
    }
    res = client.post("/users", json=user_credentials)

    new_user = res.json()

    new_user["password"] = user_credentials["password"]
    new_user["email"] = user_credentials["email"]

    assert res.status_code == 201

    return new_user


@pytest.fixture
def test_user2(client):
    user_credentials = {
        "email": "test345@gmail.com",
        "password": "test345",
        "username": "bebrta2",
    }
    res = client.post("/users", json=user_credentials)

    new_user = res.json()

    new_user["password"] = user_credentials["password"]
    new_user["email"] = user_credentials["email"]

    assert res.status_code == 201

    return new_user


@pytest.fixture
def token(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    token = res.json()
    return token


@pytest.fixture
def authorized_client(client, token):  # Мы всегда залогинены от test_user
    new_client = client
    new_client.headers = {
        **new_client.headers,
        "Authorization": f'Bearer {token["access_token"]}',
    }
    return new_client


@pytest.fixture
def test_messages(client, test_user, test_user2, session):
    messages_data = [  # Данные для создания сообщений
        {
            "title": "Test Message",
            "content": "Я рот ебал осмаловской",
            "creator_id": test_user["id"],
            "receiver_id": test_user2["id"],
        },
        {
            "title": "Test Message",
            "content": "Я рот ебал осмаловской",
            "creator_id": test_user["id"],
            "receiver_id": test_user2["id"],
        },
        {
            "title": "Test Message",
            "content": "Я рот ебал осмаловской",
            "creator_id": test_user2["id"],
            "receiver_id": test_user["id"],
        },
        {
            "title": "Test Message",
            "content": "Я рот ебал осмаловской",
            "creator_id": test_user2["id"],
            "receiver_id": test_user["id"],
        },
    ]

    def create_message_model(
            message,
    ):  # Словарь с данными для одной записки -> модель записки
        return models.Message(**message)

    message_map = map(
        create_message_model, messages_data
    )  # Преобразуем список из словарей данных для сообщений в список моделей
    messages = list(message_map)

    session.add_all(messages)
    session.commit()

    messages = session.query(models.Message).all()
    return messages


@pytest.fixture
def test_updated_data():
    return {"title": "updated title", "content": "updated content"}
