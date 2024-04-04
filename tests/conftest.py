from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.main import app

from app.schemas import message as message_schemas

from app.config import settings
from app.database import get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='module')
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='module')
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture(scope="module")  # Мега сомнительная фикстура хз
def test_user(client):
    user_credentials = {'email': 'test123@gmail.com', 'password': 'test123', 'username': 'bebrta'}
    res = client.post('/users', json=user_credentials)

    new_user = res.json()

    new_user['password'] = user_credentials['password']
    new_user['email'] = user_credentials['email']

    assert res.status_code == 201

    return new_user


@pytest.fixture(scope='module')
def token(client, test_user):
    res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    token = res.json()
    return token


@pytest.fixture()
def authorized_client(client, token):
    new_client = client
    new_client.headers = {
        **new_client.headers,
        'Authorization': f'Bearer {token["access_token"]}'
    }
    return new_client


@pytest.fixture(scope='module')
def test_messages(client, test_user, session):
    messages_data = [  # Данные для создания сообщений
        {
            'title': 'Test Message',
            'content': 'Я рот ебал осмаловской',
            'creator_id': test_user['id'],
            'receiver_id': test_user['id']
        },
        {
            'title': 'Test Message',
            'content': 'Я рот ебал осмаловской',
            'creator_id': test_user['id'],
            'receiver_id': test_user['id']
        },
        {
            'title': 'Test Message',
            'content': 'Я рот ебал осмаловской',
            'creator_id': test_user['id'],
            'receiver_id': test_user['id']
        },
        {
            'title': 'Test Message',
            'content': 'Я рот ебал осмаловской',
            'creator_id': test_user['id'],
            'receiver_id': test_user['id']
        }
    ]

    def create_message_model(message):  # Словарь с данными для одной записки -> модель записки
        return models.Message(**message)

    message_map = map(create_message_model,
                      messages_data)  # Преобразуем список из словарей данных для сообщений в список моделей
    messages = list(message_map)

    session.add_all(messages)
    session.commit()

    messages = session.query(models.Message).all()
    return messages

