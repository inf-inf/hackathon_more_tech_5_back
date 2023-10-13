from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_engine("sqlite:///database.db", echo=True)


class Base(DeclarativeBase):
    """Базовый класс ORM моделей

    :param id: primary key
    """
    id: Mapped[int] = mapped_column(primary_key=True)
