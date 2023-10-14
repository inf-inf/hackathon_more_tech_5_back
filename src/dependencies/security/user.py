from typing import Annotated
from uuid import uuid4

from fastapi import Depends, Request
from fastapi.security import APIKeyHeader


user_token_scheme = APIKeyHeader(
    name='X-Token',
    description="Токен подтвержденного пользователя"
)


def check_user_token(request: Request, token: Annotated[str, Depends(user_token_scheme)]):
    """Проверка токена пользователя

    Защита определенных операций от неправомерного использования.
    Для получения токена пользователь должен подтвердить личность с помощью
    смс, vk и тд

    Токен одноразовый, после использования, генерируется новый и записывается в request.state.new_token
    """
    new_token = uuid4()
    request.state.new_token = str(new_token)
