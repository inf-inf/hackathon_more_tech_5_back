from typing import Any, Annotated

from fastapi import APIRouter, Depends

from ..schemas.locations import FindAtmsResponse, FindOfficesResponse, FindAtmsRequest, FindOfficesRequest
from ..dependencies.logic.locations import get_locations_logic
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
