from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import APIKeyHeader

from ...models.security import UserToken


user_token_scheme = APIKeyHeader(
    name='X-Token',
    description="Токен подтвержденного пользователя"
)


def get_phone_by_token(request: Request, token: Annotated[str, Depends(user_token_scheme)]) -> str:
    """Проверка токена пользователя

    Защита определенных операций от неправомерного использования.
    Для получения токена пользователь должен подтвердить личность с помощью
    смс, vk и тд

    Токен одноразовый, после использования, генерируется новый и записывается в request.state.new_token
    """
    user_token = UserToken()
    phone = user_token.get_phone_by_token(token)
    request.state.new_token = user_token.set_new_token(phone)
    return phone
