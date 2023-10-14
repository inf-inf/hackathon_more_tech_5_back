from uuid import uuid4

from ..cache.security import TOKEN_CACHE
from ..app.exceptions import BaseApiException


class UserTokenError(BaseApiException):
    """Ошибка с токеном подтвержденного пользователя"""


class UserToken:
    """Работа с токеном доступа подтвержденного пользователя"""
    _token_cache = TOKEN_CACHE

    def set_new_token(self, phone: str) -> str:
        new_token = self._generate_token()

        duplicates = [c_token for c_token, c_phone in self._token_cache.items() if c_phone == phone]
        for duplicate in duplicates:
            del self._token_cache[duplicate]

        self._token_cache[new_token] = phone
        return new_token

    def get_phone_by_token(self, token: str) -> str:
        phone = self._token_cache.get(token, None)
        if not phone:
            raise UserTokenError('Недействительный токен')
        return phone

    @staticmethod
    def _generate_token():
        return str(uuid4())
