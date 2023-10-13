from typing import Literal, Annotated
from pydantic import BaseModel, Field
from fastapi import Query


class LocationFilter(BaseModel):
    latitude: Annotated[
        float | None,
        Field(Query(None, description="Широта пользователя", examples=[55.784435]))
    ]
    longitude: Annotated[
        float | None,
        Field(Query(None, description="Долгота пользователя", examples=[37.45707]))
    ]
    zoom: Annotated[
        int | None,
        Field(Query(None, description="Приближение на карте", examples=[5]))
    ]


class FindAtmsRequest(LocationFilter):
    """Фильтры для поиска банкоматов"""
    all_day: Annotated[
        bool | None,
        Field(Query(None, description='Работает круглосуточно', examples=['false']))
    ]
    working_now: Annotated[
        bool | None,
        Field(Query(None, description='Работает сейчас', examples=['true']))
    ]
    wheelchair: Annotated[
        bool | None,
        Field(Query(None, description='Доступен для маломобильных граждан', examples=['false']))
    ]
    blind: Annotated[
        bool | None,
        Field(Query(None, description='Оборудован для слабовидящих', examples=['false']))
    ]
    nfc_support: Annotated[
        bool | None,
        Field(Query(None, description='Поддержка NFC (бесконтактное обслуживание)', examples=['true']))
    ]
    qr_support: Annotated[
        bool | None,
        Field(Query(None, description='Поддержка QR-кода', examples=['false']))
    ]
    withdraw_currencies: Annotated[
        list[Literal['usd', 'eur', 'rub']] | None,
        Field(Query(None, description='Доступные валюты для снятия', examples=['usd']))
    ]
    deposit_currencies: Annotated[
        list[Literal['usd', 'eur', 'rub']] | None,
        Field(Query(None, description='Доступные валюты для внесения', examples=['rub']))
    ]


class FindOfficesRequest(LocationFilter):
    """Фильтры для поиска отделений"""


class Location(BaseModel):
    address: str
    latitude: float
    longitude: float
    distance: int


class Currencies(BaseModel):
    usd: bool
    eur: bool
    rub: bool


class AtmServices(BaseModel):
    all_day: Annotated[
        bool | None,
        Field(description='Работает круглосуточно', examples=['false'])
    ]
    working_now: Annotated[
        bool | None,
        Field(description='Работает сейчас', examples=['true'])
    ]
    wheelchair: Annotated[
        bool | None,
        Field(description='Доступен для маломобильных граждан', examples=['false'])
    ]
    blind: Annotated[
        bool | None,
        Field(description='Оборудован для слабовидящих', examples=['false'])
    ]
    nfc_support: Annotated[
        bool | None,
        Field(description='Поддержка NFC (бесконтактное обслуживание)', examples=['true'])
    ]
    qr_support: Annotated[
        bool | None,
        Field(description='Поддержка QR-кода', examples=['false'])
    ]


class ATMLocation(Location):
    """Данные по банкомату"""
    withdraw_currencies: Currencies
    deposit_currencies: Currencies
    services: AtmServices


class OfficeLocation(Location):
    """Данные по отделению"""


FindAtmsResponse = list[ATMLocation]

FindOfficesResponse = list[OfficeLocation]
