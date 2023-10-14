from typing import Any, Annotated

from fastapi import APIRouter, Depends, Query

from ..schemas.history import OfficeHistoryResponse
from ..dependencies.logic.history import get_history_logic
from ..logic.history import HistoryLogic

history_router = APIRouter(
    prefix="/history",
    tags=['history']
)


@history_router.get('/office', response_model=OfficeHistoryResponse, summary='Загруженность отделения')
def find_atms(office_id: Annotated[int, Query(..., alias='id', description="id отделения", examples=[1])],
              logic: Annotated[HistoryLogic, Depends(get_history_logic)],
              ) -> list[dict[str, Any]]:
    """Запрос истории по загруженности отделения банка"""
    return logic.find_office_history(office_id)
