from typing import Any, Annotated

from fastapi import APIRouter, Depends

from ..dependencies.logic.user import get_user_logic
from ..logic.user import UserLogic
from ..schemas.user import SendSmsRequest, SendSmsResponse, ConfirmSmsRequest, FavoritesAddRequest
from ..dependencies.security.user import get_phone_by_token


user_router = APIRouter(
    prefix="/user",
    tags=['user']
)


@user_router.post('/request/sms', summary='Запросить смс для подтверждения', response_model=SendSmsResponse)
def request_sms(data: SendSmsRequest,
                logic: Annotated[UserLogic, Depends(get_user_logic)]
                ) -> dict[str, Any]:
    return logic.request_sms(data.phone)


@user_router.post('/confirm/sms', summary='Подтвердить номер по коду из смс')
def confirm_sms(data: ConfirmSmsRequest,
                logic: Annotated[UserLogic, Depends(get_user_logic)],
                ) -> dict[str, Any]:
    return {'token': logic.confirm_sms(data.code)}


@user_router.post('/favorites/add', summary='Добавить локацию в избранное')
def favorites_add(data: FavoritesAddRequest,
                  logic: Annotated[UserLogic, Depends(get_user_logic)],
                  user_phone: Annotated[str, Depends(get_phone_by_token)]
                  ) -> bool:
    return logic.favorites_add(data.location_type, data.location_id, user_phone)


@user_router.get('/favorites/get', summary='Получить сохраненные локации')
def favorites_get(logic: Annotated[UserLogic, Depends(get_user_logic)],
                  user_phone: Annotated[str, Depends(get_phone_by_token)]
                  ) -> list[dict[str, Any]]:
    return logic.favorites_get(user_phone)
