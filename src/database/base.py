from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


engine = create_engine("sqlite:///database.db", echo=True, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Базовый класс ORM моделей

    :param id: primary key
    """
    id: Mapped[int] = mapped_column(primary_key=True)
