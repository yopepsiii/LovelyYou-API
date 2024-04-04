from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app

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


@pytest.fixture(scope='module')
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token["access_token"]}'
    }
    return client
