from sqlalchemy import Column, Integer, Text
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


EMBEDDING_LENGTH = 768


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    embedding = Column(Vector(EMBEDDING_LENGTH), nullable=False)
