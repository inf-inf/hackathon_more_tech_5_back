from typing import Any, Annotated

from fastapi import APIRouter, Depends, Query

from ..schemas.locations import (
    FindAtmsResponse,
    FindOfficesResponse,
    FindAtmsRequest,
    FindOfficesRequest,
    GetATMReviewsResponse,
    GetOfficeReviewsResponse
)
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


@locations_router.get('/get_atm_reviews', response_model=GetATMReviewsResponse, summary='Отзывы о банкомате')
def get_atm_reviews(atm_id: Annotated[int, Query(alias='atmId')],
                    logic: Annotated[LocationsLogic, Depends(get_locations_logic)],
                    ) -> list[dict[str, Any]]:
    """Получить список отзывов о банкомате"""
    return logic.get_atm_reviews(atm_id)


@locations_router.get('/get_office_reviews', response_model=GetOfficeReviewsResponse, summary='Отзывы об отделении')
def get_office_reviews(office_id: Annotated[int, Query(alias='officeId')],
                       logic: Annotated[LocationsLogic, Depends(get_locations_logic)],
                       ) -> list[dict[str, Any]]:
    """Получить список отзывов об отделении банка"""
    return logic.get_office_reviews(office_id)


@locations_router.get('/office_visit/request', summary='Запросить посещение отделения')
def request_office_visit(office_id: Annotated[int, Query(alias='officeId',
                                                         description="Идентификатор отделения банка")],
                         logic: Annotated[LocationsLogic, Depends(get_locations_logic)],
                         ) -> dict[str, Any]:
    """Получить доступное время для записи в отделение банка

    Регистрация доступна только на текущий день
    """
    return logic.request_office_visit(office_id)


@locations_router.post('/office_visit/register', summary='Записаться на посещение отделения')
def register_office_visit(logic: Annotated[LocationsLogic, Depends(get_locations_logic)],
                          user_phone: Annotated[str, Depends(get_phone_by_token)],
                          office_id: Annotated[int, Query(alias='officeId',
                                                          description="Идентификатор отделения банка")],
                          selected_time: Annotated[str, Query(alias='selectedTime',
                                                              description="Выбранное время посещения")]
                          ) -> dict[str, Any]:
    """Запись в электронную очередь отделения банка

    Функционал доступен авторизованным клиентам банка, либо пользователям,
    прошедшим процедуру подтверждения личности (смс, vk, ...)

    Возвращает регистрационный номер в очереди и информацию для памятки пользователю:
    выбранная дата и время, адрес отделения, номер телефона (на который был оформлен прием)
    """
    return logic.register_office_visit(user_phone, office_id, selected_time)
