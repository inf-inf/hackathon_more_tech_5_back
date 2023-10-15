from typing import Annotated, Any

from fastapi import Query
from pydantic import BaseModel, Field, model_validator, field_serializer

from .base import BaseOrmModel
from ..database.models import Week


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
    avg_rating: Annotated[
        int | None,
        Field(None, alias="avgRating", description="Средний рейтинг офиса (от 10 до 50)", examples=["44"])
    ]
    avg_service_time: Annotated[
        int | None,
        Field(
            Query(
                None,
                alias="avgServiceTime",
                description="Среднее время обслуживания клиента",
                examples=["4"]
            )
        )
    ]
    count_clients_now: Annotated[
        int | None,
        Field(
            Query(
                None,
                alias="countClientsNow",
                description="Количество клиентов прямо сейчас ожидающих в офисе в очереди",
                examples=["7"]
            )
        )
    ]
    with_ramp: Annotated[
        bool | None,
        Field(Query(None, alias="withRamp", description="Имеется ли пандус", examples=["true"]))
    ]
    prime: Annotated[
        bool | None,
        Field(Query(None, description="Нужно ли обслуживание PRIME клиентов", examples=["true"]))
    ]
    vip: Annotated[
        bool | None,
        Field(Query(None, description="Нужно ли обслуживание VIP клиентов", examples=["true"]))
    ]
    rko: Annotated[
        bool | None,
        Field(Query(None, description="Нужен ли РКО", examples=["true"]))
    ]
    suo: Annotated[
        bool | None,
        Field(Query(None, description="Нужен ли СУО", examples=["true"]))
    ]
    kep: Annotated[
        bool | None,
        Field(Query(None, description="Нужен ли КЭП", examples=["true"]))
    ]
    withdraw_currencies: Annotated[
        list[str] | None,
        Field(Query(None, alias="withdrawCurrencies", description="Какую валюту нужно вывести", examples=["rub"]))
    ]
    deposit_currencies: Annotated[
        list[str] | None,
        Field(Query(None, alias="depositCurrencies", description="Какую валюту нужно вывести", examples=["rub, usd"]))
    ]

    @field_serializer('withdraw_currencies')
    def serialize_withdraw_currencies(self, withdraw_currencies: str | None, _info):
        return [currency.strip() for currency in withdraw_currencies.split(',')] if withdraw_currencies else None

    @field_serializer('deposit_currencies')
    def serialize_deposit_currencies(self, deposit_currencies: str | None, _info):
        return [currency.strip() for currency in deposit_currencies.split(',')] if deposit_currencies else None


class Currencies(BaseModel):
    usd: Annotated[bool, Field(description="Доллары", examples=['false'])]
    eur: Annotated[bool, Field(description="Евро", examples=['false'])]
    rub: Annotated[bool, Field(description="Рубли", examples=['true'])]


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
    all_time: Annotated[bool, Field(alias="allTime", description="Работает ли круглосуточно", examples=["false"])]
    days: Annotated[
        list[str | None],
        Field(
            None,
            description="Список времени работы по дням недели (0 элемент - понедельник, 7 элемент - воскресенье",
            examples=['["09:00-17:00", "09:00-17:00", "09:00-17:00", "09:00-17:00", "09:00-17:00", null, null]']
        )
    ]

    @model_validator(mode="before")
    @classmethod
    def _formatting(cls, data: Any) -> Any:
        if isinstance(data, Week):
            return {
                "all_time": data.all_time,
                "days": [data.monday, data.tuesday, data.wednesday, data.thursday, data.friday,
                         data.saturday, data.sunday]
            }
        return data

    @model_validator(mode="after")
    def _check_nones(self) -> 'WeekModel | None':
        if not any([self.all_time, *self.days]):
            return None
        return self


class ATMServicesModel(BaseOrmModel):
    currency_input: Annotated[
        Currencies,
        Field(alias="currencyInput", description="Информация о валютах, которые может принимать банкомат")
    ]
    currency_output: Annotated[
        Currencies,
        Field(alias="currencyOutput", description="Информация о валютах, которые может выдавать банкомат")
    ]
    wheelchair: Annotated[bool, Field(description="Доступен для маломобильных граждан", examples=["true"])]
    blind: Annotated[bool, Field(description="Оборудован для слабовидящих", examples=["true"])]
    nfc: Annotated[bool, Field(description="Поддержка NFC (бесконтактное обслуживание)", examples=["true"])]
    qr_code: Annotated[bool, Field(alias='qrCode', description="Поддержка работы с QR-кодами", examples=["true"])]


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


GetReviewsResponse = list[ReviewsModel]


class PostReviewRequest(BaseModel):
    location_id: int
    review: Annotated[str, Field(max_length=500, description='Отзыв')]
    stars: Annotated[int, Field(ge=1, le=5, description='Количество звезд (от 1 до 5)')]


class PostReviewResponse(BaseModel):
    msg: str = 'Ваш отзыв отправлен на модерацию'
