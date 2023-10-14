from uuid import uuid4


class UserToken:
    """Работа с токеном доступа подтвержденного пользователя"""

    def set_new_token(self, phone: str) -> str:
        new_token = self._generate_token()
        # TODO save phone + new_token to cache
        return new_token

    def get_phone_by_token(self, token: str) -> str:
        # TODO get self._phone from cache by token
        return 'phone'

    @staticmethod
    def _generate_token():
        return str(uuid4())
