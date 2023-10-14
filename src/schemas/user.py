from datetime import datetime

from pydantic import BaseModel


class SendSmsRequest(BaseModel):
    phone: str


class SendSmsResponse(BaseModel):
    phone: str
    sent_time: datetime
    expiration_time: datetime


class ConfirmSmsRequest(BaseModel):
    code: str
