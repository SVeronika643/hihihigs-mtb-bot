__all__ = ["User","Base",]

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, VARCHAR, Text

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_table"
    user_id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255), unique=False, nullable=False)
    tutorcode = Column(VARCHAR(6), nullable=True)
    subscribe = Column(VARCHAR(6), nullable=True)
    extra = Column(Text, unique=False)