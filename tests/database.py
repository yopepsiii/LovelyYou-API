import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette.testclient import TestClient

from app import models
from app.config import settings
from app.database import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = (
    f"postgresql:"
    f"//{settings.database_username}"
    f":{settings.database_password}"
    f"@{settings.database_hostname}"
    f":{settings.database_port}"
    f"/{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
