from typing import Any
import random

from ..app.exceptions import BaseApiException
from ..cache.sms import SMS_CACHE


class SMSError(BaseApiException):
    """Ошибка СМС"""


class SMS:
    _sms_cache = SMS_CACHE

    def send(self, phone: str, text: str) -> None:
        ...

    @staticmethod
    def generate_code() -> str:
        return str(random.randint(1000, 9999))

    def save_sms(self, code: str, sms_info: dict[str, Any]):
        code = '7777'   # mock
        self._sms_cache[code] = sms_info

    def get_sms(self, code: str):
        sms_info = self._sms_cache.get(code)
        if not sms_info:
            raise SMSError('Неверный код')
        return sms_info
