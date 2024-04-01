import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db

client = TestClient(app)



SQL_ALCHEMY_DATABASE_URL = (
    f"postgresql:"
    f"//{settings.database_username}"
    f":{settings.database_password}"
    f"@{settings.database_hostname}"
    f":{settings.database_port}"
    f"/{settings.database_name}"
)

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()














def test_root():
    res = client.get("/")
    print(res.json())


def test_create_user():
    res = client.post("/users/", json={"username": "bebra", "email": "bebra228@gmail.com", "password": "AloHuis"})
    print(res.json())
    assert res.status_code == 201
