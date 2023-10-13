from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ATM(Base):
    """ORM модель для банкоматов

    :param address: полный адрес
    :param latitude: географическая широта
    :param longitude: географическая долгота
    :param avg_rating: средний рейтинг банкомата
    """
    __tablename__ = "atm"

    address: Mapped[str] = mapped_column(String(250), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    avg_rating: Mapped[int] = mapped_column(Integer)


class ATMReviews(Base):
    """ORM модель для отзывов на банкоматы

    :param atm_id: внешний ключ на atm.id
    :param rating: оценка (числовая) конкретного банкомата
    :param content: текстовый отзыв от пользователя
    """
    __tablename__ = "atm_reviews"

    atm_id: Mapped[int] = mapped_column(ForeignKey(ATM.id), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str | None] = mapped_column(String(200))


class Office(Base):
    """ORM модель для офисов

    :param address: полный адрес
    :param latitude: географическая широта
    :param longitude: географическая долгота
    :param avg_rating: средний рейтинг офиса
    :param with_ramp: есть ли пандус (True - есть)
    """
    __tablename__ = "office"

    address: Mapped[str] = mapped_column(String(250), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    avg_rating: Mapped[int | None] = mapped_column(Integer)
    with_ramp: Mapped[bool] = mapped_column(Boolean, default=False, server_default=false(), nullable=False)


class OfficeReviews(Base):
    """ORM модель для отзывов на офисы

    :param office_id: внешний ключ на office.id
    :param rating: оценка (числовая) конкретного офиса
    :param content: текстовый отзыв от пользователя
    """
    __tablename__ = "office_reviews"

    office_id: Mapped[int] = mapped_column(ForeignKey(Office.id), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(String(200))


class Week(Base):
    """ORM модель для информации о рабочей неделе

    :param office_id: внешний ключ на office.id
    :param monday: время работы офиса в понедельник (через "-", пример "09:00-18:00")
    :param tuesday: время работы офиса во вторник (через "-", пример "09:00-18:00")
    :param wednesday: время работы офиса в среду (через "-", пример "09:00-18:00")
    :param thursday: время работы офиса в четверг (через "-", пример "09:00-18:00")
    :param friday: время работы офиса в пятницу (через "-", пример "09:00-18:00")
    :param saturday: время работы офиса в субботу (через "-", пример "09:00-18:00")
    :param sunday: время работы офиса в воскресенье (через "-", пример "09:00-18:00")
    """
    __tablename__ = "week"

    office_id: Mapped[int] = mapped_column(ForeignKey(Office.id), nullable=False)
    monday: Mapped[str | None] = mapped_column(String(15))
    tuesday: Mapped[str | None] = mapped_column(String(15))
    wednesday: Mapped[str | None] = mapped_column(String(15))
    thursday: Mapped[str | None] = mapped_column(String(15))
    friday: Mapped[str | None] = mapped_column(String(15))
    saturday: Mapped[str | None] = mapped_column(String(15))
    sunday: Mapped[str | None] = mapped_column(String(15))
