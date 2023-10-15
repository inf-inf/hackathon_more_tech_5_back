from typing import Annotated, Literal
from datetime import datetime

from pydantic import BaseModel, Field

from .base import BaseCamelModel


class SendSmsRequest(BaseModel):
    phone: str


class SendSmsResponse(BaseCamelModel):
    phone: str
    sent_time: Annotated[datetime, Field(alias='sentTime')]
    expiration_time: Annotated[datetime, Field(alias='expirationTime')]


class ConfirmSmsRequest(BaseModel):
    code: str


class FavoritesAddRequest(BaseCamelModel):
    location_type: Annotated[
        Literal['office', 'atm'], Field(alias='type', description='Тип локации: отделение банка или банкомат')
    ]
    location_id: Annotated[
        int, Field(alias='id', description='Идентификатор локации', examples=[657])
    ]
