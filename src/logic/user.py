from typing import TypedDict
from datetime import datetime, timedelta

from ..models.sms import SMS, SMSError
from ..models.security import UserToken


class SentSmsInfo(TypedDict):
    phone: str
    sent_time: datetime
    expiration_time: datetime


class UserLogic:
    """Логика работы с пользователем"""
    def __init__(self):
        self._sms = SMS()
        self._sms_lifetime = timedelta(minutes=5)
        self._user_token = UserToken()

    def request_sms(self, phone: str) -> SentSmsInfo:
        """Запросить смс для подтверждения"""
        code = self._sms.generate_code()
        self._sms.send(phone, code)
        sent_time = datetime.now()
        sms_info = SentSmsInfo(phone=phone, sent_time=sent_time, expiration_time=sent_time + self._sms_lifetime)
        self._sms.save_sms(code, sms_info)
        return sms_info

    def confirm_sms(self, code: str) -> str:
        """Подтвердить номер по коду из смс"""
        sms_info: SentSmsInfo = self._sms.get_sms(code)
        if sms_info['expiration_time'] < datetime.now():
            raise SMSError('Код устарел')
        return self._user_token.set_new_token(sms_info['phone'])
