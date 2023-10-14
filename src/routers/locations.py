from typing import Any, Annotated

from fastapi import APIRouter, Depends, Query

from ..schemas.locations import FindAtmsResponse, FindOfficesResponse, FindAtmsRequest, FindOfficesRequest
from ..dependencies.logic.locations import get_locations_logic
from ..dependencies.security.user import get_phone_by_token
from ..logic.locations import LocationsLogic

locations_router = APIRouter(
    prefix="/locations",
    tags=['locations']
)


@locations_router.get('/find_atms', response_model=FindAtmsResponse, summary='Поиск банкоматов')
def find_atms(filter_data: Annotated[FindAtmsRequest, Depends()],
              logic: Annotated[LocationsLogic, Depends(get_locations_logic)],
              ) -> list[dict[str, Any]]:
    """Поиск оптимальных банкоматов с применением фильтров"""
    return logic.find_atms(filter_data.model_dump())


@locations_router.get('/find_offices', response_model=FindOfficesResponse, summary='Поиск отделений')
def find_offices(filter_data: Annotated[FindOfficesRequest, Depends()],
                 logic: Annotated[LocationsLogic, Depends(get_locations_logic)],
                 ) -> list[dict[str, Any]]:
    """Поиск оптимальных отделений с применением фильтров"""
    return logic.find_offices(filter_data.model_dump())


@locations_router.get('/office_visit/request', summary='Запросить посещение отделения')
def request_office_visit(office_id: Annotated[int, Query(description="Идентификатор отделения банка")],
                         logic: Annotated[LocationsLogic, Depends(get_locations_logic)],
                         ) -> dict[str, Any]:
    """Получить доступное время для записи в отделение банка

    Регистрация доступна только на текущий день
    """
    return logic.request_office_visit(office_id)


@locations_router.post('/office_visit/register', summary='Записаться на посещение отделения')
def register_office_visit(logic: Annotated[LocationsLogic, Depends(get_locations_logic)],
                          user_phone: Annotated[str, Depends(get_phone_by_token)]) -> dict[str, Any]:
    """Запись в электронную очередь отделения банка

    Функционал доступен авторизованным клиентам банка, либо пользователям,
    прошедшим процедуру подтверждения личности (смс, vk, ...)
    """
    return logic.register_office_visit(user_phone)
