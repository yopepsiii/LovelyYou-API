from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class User(Base):
    __tablename__: str = 'Users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)


class Message(Base):
    __tablename__: str = 'Messages'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, server_default="Название записки")
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
