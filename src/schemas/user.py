from typing import Annotated, Literal
from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseCamelModel


class SendSmsRequest(BaseModel):
    phone: Annotated[str, Field(description="Телефон, на который нужно отправить СМС", examples=["+79999999999"])]


class SendSmsResponse(BaseCamelModel):
    phone: Annotated[str, Field(description="Телефон, на который было отправлено СМС", examples=["+79999999999"])]
    sent_time: Annotated[datetime, Field(alias='sentTime')]
    expiration_time: Annotated[datetime, Field(alias='expirationTime')]


class ConfirmSmsRequest(BaseModel):
    code: Annotated[str, Field(description="Код подтверждения (для авторизации)", examples=["555333"])]


class FavoritesAddRequest(BaseCamelModel):
    location_type: Annotated[
        Literal['office', 'atm'], Field(alias='type', description='Тип локации: отделение банка или банкомат')
    ]
    location_id: Annotated[
        int, Field(alias='id', description='Идентификатор локации', examples=[657])
    ]
