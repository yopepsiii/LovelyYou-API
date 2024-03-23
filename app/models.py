from sqlalchemy import Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class User(Base):
    __tablename__: str = "Users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Message(Base):
    __tablename__: str = "Messages"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, server_default="Название записки")
    content = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    creator_id = Column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    receiver_id = Column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    creator = relationship("User", foreign_keys=[creator_id])  # type: ignore
    receiver = relationship("User", foreign_keys=[receiver_id])  # type: ignore
