from typing import Any, Annotated

from fastapi import APIRouter, Depends, Query

from ..schemas.history import OfficeHistoryResponse
from ..dependencies.logic.history import get_history_logic
from ..logic.history import HistoryLogic

history_router = APIRouter(
    prefix="/history",
    tags=['history']
)


@history_router.get('/office', response_model=OfficeHistoryResponse, summary='Поиск банкоматов')
def find_atms(id: Annotated[int, Query(..., description="id отделения", examples=[1])],
              logic: Annotated[HistoryLogic, Depends(get_history_logic)],
              ) -> list[dict[str, Any]]:
    """Поиск оптимальных банкоматов с применением фильтров"""
    return logic.find_office_history(id)
