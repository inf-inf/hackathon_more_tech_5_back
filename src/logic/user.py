from typing import TypedDict
from datetime import datetime, timedelta

from ..models.sms import SMS


class SentSmsInfo(TypedDict):
    phone: str
    sent_time: datetime
    expiration_time: datetime


class UserLogic:
    """Логика работы с пользователем"""
    def __init__(self):
        self._sms = SMS()
        self._sms_lifetime = timedelta(minutes=5)

    def request_sms(self, phone: str) -> SentSmsInfo:
        """Запросить смс для подтверждения"""
        code = self._sms.generate_code()
        self._sms.send(phone, code)
        sent_time = datetime.now()
        sms_info = SentSmsInfo(phone=phone, sent_time=sent_time, expiration_time=sent_time + self._sms_lifetime)
        # TODO save sms_info
        return sms_info

    def confirm_sms(self, code: str):
        """Подтвердить номер по коду из смс"""
        ...
