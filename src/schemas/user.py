from typing import Annotated
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
