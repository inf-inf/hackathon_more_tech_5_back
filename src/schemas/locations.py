from typing import Annotated, Any

from fastapi import Query
from pydantic import BaseModel, Field, model_validator, field_serializer

from .base import BaseOrmModel


class LocationFilter(BaseModel):
    latitude: Annotated[
        float,
        Field(Query(description="Широта пользователя", examples=[55.784435]))
    ]
    longitude: Annotated[
        float,
        Field(Query(description="Долгота пользователя", examples=[37.45707]))
    ]
    initial_latitude: Annotated[
        float,
        Field(Query(alias='initialLatitude', description="Базовая широта пользователя", examples=[55.784435]))
    ]
    initial_longitude: Annotated[
        float,
        Field(Query(alias='initialLongitude', description="Базовая долгота пользователя", examples=[37.45707]))
    ]
    zoom: Annotated[
        float,
        Field(Query(description="Приближение на карте", examples=[16.45]))
    ]


class FindAtmsRequest(LocationFilter):
    """Фильтры для поиска банкоматов"""
    all_day: Annotated[
        bool | None,
        Field(Query(None, alias='allDay', description='Работает круглосуточно', examples=['false']))
    ]
    avg_rating: Annotated[
        int | None,
        Field(
            Query(
                None,
                alias='avgRating',
                description='Средний рейтинг банкомата, минимальное значение',
                examples=['true']
            )
        )
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
        Field(
            Query(
                None,
                alias='nfcSupport',
                description='Поддержка NFC (бесконтактное обслуживание)',
                examples=['true']
            )
        )
    ]
    qr_support: Annotated[
        bool | None,
        Field(Query(None, alias='qrSupport', description='Поддержка QR-кода', examples=['false']))
    ]
    withdraw_currencies: Annotated[
        str | None,
        Field(
            Query(
                None,
                alias='withdrawCurrencies',
                description='Доступные валюты для снятия (usd, eur, rub)',
                examples=['usd, rub']
            )
        )
    ]
    deposit_currencies: Annotated[
        str | None,
        Field(
            Query(
                None,
                alias='depositCurrencies',
                description='Доступные валюты для внесения (usd, eur, rub)',
                examples=['rub']
            )
        )
    ]

    @field_serializer('withdraw_currencies')
    def serialize_withdraw_currencies(self, withdraw_currencies: str | None, _info):
        return [currency.strip() for currency in withdraw_currencies.split(',')] if withdraw_currencies else None

    @field_serializer('deposit_currencies')
    def serialize_deposit_currencies(self, deposit_currencies: str | None, _info):
        return [currency.strip() for currency in deposit_currencies.split(',')] if deposit_currencies else None


class FindOfficesRequest(LocationFilter):
    """Фильтры для поиска отделений"""


class Currencies(BaseModel):
    usd: bool
    eur: bool
    rub: bool


class AtmServices(BaseModel):
    all_day: Annotated[
        bool | None,
        Field(alias='allDay', description='Работает круглосуточно', examples=['false'])
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
        Field(alias='nfcSupport', description='Поддержка NFC (бесконтактное обслуживание)', examples=['true'])
    ]
    qr_support: Annotated[
        bool | None,
        Field(alias='qrSupport', description='Поддержка QR-кода', examples=['false'])
    ]


class WeekModel(BaseOrmModel):
    all_time: bool = Field(alias='allTime')
    monday: str | None
    tuesday: str | None
    wednesday: str | None
    thursday: str | None
    friday: str | None
    saturday: str | None
    sunday: str | None


class ATMServicesModel(BaseOrmModel):
    currency_input: Currencies = Field(alias='currencyInput')
    currency_output: Currencies = Field(alias='currencyOutput')
    wheelchair: bool
    blind: bool
    nfc: bool
    qr_code: bool = Field(alias='qrCode')


class ATMModel(BaseOrmModel):
    id: int
    distance: float | None = None
    address: str
    latitude: float
    longitude: float
    avg_rating: int | None = Field(None, alias='avgRating')
    review_count: int = Field(None, alias='reviewCount')
    service_info: ATMServicesModel = Field(alias='serviceInfo')
    week_info: WeekModel = Field(alias='weekInfo')

    @model_validator(mode="before")
    @classmethod
    def _check_distance(cls, data: Any) -> Any:
        if hasattr(data, "ATM") and hasattr(data, "distance"):
            data.ATM.distance = data.distance
        return data.ATM


class OfficeServicesModel(BaseOrmModel):
    currency_input: Currencies = Field(alias='currencyInput')
    currency_output: Currencies = Field(alias='currencyOutput')
    with_ramp: bool = Field(alias='withRamp')
    prime: bool
    vip: bool
    rko: bool
    suo: bool
    kep: bool


class OfficeModel(BaseOrmModel):
    id: int
    distance: float
    address: str
    latitude: float
    longitude: float
    avg_rating: int | None = Field(None, alias='avgRating')
    review_count: int = Field(alias='reviewCount')
    avg_service_time: int = Field(alias="avgServiceTime")
    count_clients_now: int = Field(alias="countClientsNow")
    time_wait: int = Field(alias="timeWait")
    week_info_fiz: WeekModel | None = Field(None, alias='weekInfoFiz')
    week_info_yur: WeekModel | None = Field(None, alias='weekInfoYur')
    service_info: OfficeServicesModel = Field(alias='serviceInfo')

    @model_validator(mode="before")
    @classmethod
    def _check_distance(cls, data: Any) -> Any:
        if hasattr(data, "Office") and hasattr(data, "distance") and hasattr(data, "time_wait"):
            data.Office.distance = data.distance
            data.Office.time_wait = data.time_wait
        return data.Office


FindAtmsResponse = list[ATMModel]
FindOfficesResponse = list[OfficeModel]


class ReviewsModel(BaseOrmModel):
    rating: int
    content: str | None


GetATMReviewsResponse = list[ReviewsModel]
GetOfficeReviewsResponse = list[ReviewsModel]
