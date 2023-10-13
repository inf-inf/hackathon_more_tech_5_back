from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


engine = create_engine("sqlite://", echo=True)


class Base(DeclarativeBase):
    """Базовый класс ORM моделей"""
