from typing import Any, Annotated

from fastapi import APIRouter, Depends

from ..dependencies.logic.user import get_user_logic
from ..logic.user import UserLogic
from ..schemas.user import SendSmsRequest, SendSmsResponse


user_router = APIRouter(
    prefix="/user",
    tags=['user']
)


@user_router.post('/request/sms', summary='Запросить смс для подтверждения', response_model=SendSmsResponse)
def request_sms(data: SendSmsRequest,
                logic: Annotated[UserLogic, Depends(get_user_logic)]) -> dict[str, Any]:
    return logic.request_sms(data.phone)


@user_router.post('/confirm/sms', summary='Подтвердить номер по коду из смс')
def confirm_sms() -> dict[str, Any]:
    return {}
