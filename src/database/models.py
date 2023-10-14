from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ATM(Base):
    """ORM модель для банкоматов

    :param address: полный адрес
    :param latitude: географическая широта
    :param longitude: географическая долгота
    :param avg_rating: средний рейтинг банкомата
    :param service_info_id: внешний ключ на ATMService (информация о возможностях (услугах) в банкомате
    :param week_info_id: информация о времени работы банкомата по дням недели
    """
    __tablename__ = "atm"

    address: Mapped[str] = mapped_column(String(250), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    avg_rating: Mapped[int | None] = mapped_column(Integer)
    service_info_id: Mapped[int] = mapped_column(ForeignKey("atm_service.id"), nullable=False)
    week_info_id: Mapped[int] = mapped_column(ForeignKey("week.id"), nullable=False)

    reviews: Mapped[list["ATMReviews"]] = relationship(back_populates="atm")
    service_info: Mapped["ATMServices"] = relationship()
    week_info: Mapped["Week"] = relationship()


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

    atm: Mapped["ATM"] = relationship(back_populates="reviews")


class ATMServices(Base):
    """ORM модель возможностей (услуг) конкретного банкомата

    :param currency_input_id: информация о валюте, которую может принять банкомат
    :param currency_output_id: информация о валюте, которую может выдать банкомат
    :param wheelchair: доступен ли для маломобильных граждан
    :param blind: оборудован для слабовидящих
    :param nfc: есть поддержка NFC
    :param qr_code: есть поддержка работы с QR-кодами
    """
    __tablename__ = "atm_service"

    currency_input_id: Mapped[int] = mapped_column(ForeignKey("currency.id"), nullable=False)
    currency_output_id: Mapped[int] = mapped_column(ForeignKey("currency.id"), nullable=False)
    wheelchair: Mapped[bool] = mapped_column(Boolean, nullable=False)
    blind: Mapped[bool] = mapped_column(Boolean, nullable=False)
    nfc: Mapped[bool] = mapped_column(Boolean, nullable=False)
    qr_code: Mapped[bool] = mapped_column(Boolean, nullable=False)

    currency_input: Mapped["Currency"] = relationship(foreign_keys=[currency_input_id])
    currency_output: Mapped["Currency"] = relationship(foreign_keys=[currency_output_id])


class Office(Base):
    """ORM модель для офисов

    :param address: полный адрес
    :param latitude: географическая широта
    :param longitude: географическая долгота
    :param avg_rating: средний рейтинг офиса
    :param with_ramp: есть ли пандус (True - есть)
    :param week_info_fiz_id: информация о времени работы отделения для физ. лиц
    :param week_info_yur_id: информация о времени работы отделения для юр. лиц
    :param service_info_id: информация о предоставляемых услугах в конкретном офисе
    """
    __tablename__ = "office"

    address: Mapped[str] = mapped_column(String(250), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    avg_rating: Mapped[int | None] = mapped_column(Integer)
    week_info_fiz_id: Mapped[int] = mapped_column(ForeignKey("week.id"), nullable=False)
    week_info_yur_id: Mapped[int] = mapped_column(ForeignKey("week.id"), nullable=False)
    service_info_id: Mapped[int] = mapped_column(ForeignKey("office_service.id"), nullable=False)

    reviews: Mapped[list["OfficeReviews"]] = relationship(back_populates="office")
    week_info_fiz: Mapped["Week"] = relationship(foreign_keys=[week_info_fiz_id])
    week_info_yur: Mapped["Week"] = relationship(foreign_keys=[week_info_yur_id])
    service_info: Mapped["OfficeServices"] = relationship()


class OfficeReviews(Base):
    """ORM модель для отзывов на офисы

    :param office_id: внешний ключ на office.id
    :param rating: оценка (числовая) конкретного офиса
    :param content: текстовый отзыв от пользователя
    """
    __tablename__ = "office_reviews"

    office_id: Mapped[int] = mapped_column(ForeignKey(Office.id), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str | None] = mapped_column(String(200))

    office: Mapped["Office"] = relationship(back_populates="reviews")


class OfficeServices(Base):
    """ORM модель услуг, которые могут быть у конкретного офиса

    :param currency_input_id: информация о валюте, которую могут принимать в отделении банка
    :param currency_output_id: информация о валюте, которую могут выдавать в отделении банка
    :param rko: наличие РКО
    :param suo: наличие СУО
    :param kep: есть ли возможность выдать КЭП
    """
    __tablename__ = "office_service"

    currency_input_id: Mapped[int] = mapped_column(ForeignKey("currency.id"), nullable=False)
    currency_output_id: Mapped[int] = mapped_column(ForeignKey("currency.id"), nullable=False)
    with_ramp: Mapped[bool] = mapped_column(Boolean, default=False, server_default=false(), nullable=False)
    rko: Mapped[bool] = mapped_column(Boolean, nullable=False)
    suo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    kep: Mapped[bool] = mapped_column(Boolean, nullable=False)

    currency_input: Mapped["Currency"] = relationship(foreign_keys=[currency_input_id])
    currency_output: Mapped["Currency"] = relationship(foreign_keys=[currency_output_id])


class Week(Base):
    """ORM модель для информации о рабочей неделе

    :param all_time: True - значит офис/банкомат работает круглосуточно (поле нужно смотреть в приоритете перед другими)
    :param monday: время работы офиса/банкомата в понедельник (через "-", пример "09:00-18:00")
    :param tuesday: время работы офиса/банкомата во вторник (через "-", пример "09:00-18:00")
    :param wednesday: время работы офиса/банкомата в среду (через "-", пример "09:00-18:00")
    :param thursday: время работы офиса/банкомата в четверг (через "-", пример "09:00-18:00")
    :param friday: время работы офиса/банкомата в пятницу (через "-", пример "09:00-18:00")
    :param saturday: время работы офиса/банкомата в субботу (через "-", пример "09:00-18:00")
    :param sunday: время работы офиса/банкомата в воскресенье (через "-", пример "09:00-18:00")
    """
    __tablename__ = "week"

    all_time: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
    monday: Mapped[str | None] = mapped_column(String(15))
    tuesday: Mapped[str | None] = mapped_column(String(15))
    wednesday: Mapped[str | None] = mapped_column(String(15))
    thursday: Mapped[str | None] = mapped_column(String(15))
    friday: Mapped[str | None] = mapped_column(String(15))
    saturday: Mapped[str | None] = mapped_column(String(15))
    sunday: Mapped[str | None] = mapped_column(String(15))


class Currency(Base):
    """ORM модель для информации о допустимой валюте

    :param rub: принимаются ли рубли
    :param usd: принимаются ли доллары
    :param eur: принимаются ли евро
    """
    __tablename__ = "currency"

    rub: Mapped[bool] = mapped_column(Boolean, nullable=False)
    usd: Mapped[bool] = mapped_column(Boolean, nullable=False)
    eur: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Users(Base):
    """ORM модель пользователя (для облегченной авторизации и персональных возможностей)

    :param phone: номер телефона пользователя (для идентификации)
    """
    __tablename__ = "users"

    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    favorites_atms: Mapped[list["UserFavoritesATM"]] = relationship(back_populates="user")
    favorites_offices: Mapped[list["UserFavoritesOffice"]] = relationship(back_populates="user")
    own_addresses: Mapped[list["UserAddresses"]] = relationship(back_populates="user")


class UserAddresses(Base):
    """ORM модель сохраненных адресов пользователя

    :param user_id: пользователь (ORM Users)
    :param address: сохраненный пользователем адрес
    :param tag: личный тег пользователя (для фильтрации и удобного поиска своих адресов)
    """
    __tablename__ = "user_addresses"

    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id), nullable=False)
    address: Mapped[str] = mapped_column(String(250))
    tag: Mapped[str] = mapped_column(String(30))

    user: Mapped["Users"] = relationship(back_populates="own_addresses")


class UserFavoritesATM(Base):
    """ORM модель избранных банкоматов пользователей

    :param user_id: пользователь (ORM Users)
    :param atm_id: избранный банкомат пользователя
    """
    __tablename__ = "user_favorites_atm"

    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id), nullable=False)
    atm_id: Mapped[int] = mapped_column(ForeignKey(ATM.id), nullable=False)

    user: Mapped["Users"] = relationship(back_populates="favorites_atms")
    atm: Mapped[ATM] = relationship()


class UserFavoritesOffice(Base):
    """ORM модель избранных отделений пользователя

    :param user_id: пользователь (ORM Users)
    :param office_id: избранное пользователем отделение банка
    """
    __tablename__ = "user_favorites_office"

    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id), nullable=False)
    office_id: Mapped[str] = mapped_column(ForeignKey(Office.id), nullable=False)

    user: Mapped["Users"] = relationship(back_populates="favorites_offices")
    office: Mapped[Office] = relationship()
