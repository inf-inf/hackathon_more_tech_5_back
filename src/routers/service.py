from fastapi import APIRouter

from ..schemas.service import HealthcheckResponse

service_router = APIRouter(
    prefix="/service",
    tags=['service']
)


@service_router.get('/healthcheck', response_model=HealthcheckResponse, summary='Проверка работоспособности API')
async def healthcheck() -> dict[str, str]:
    """Базовая проверка доступности API для мониторинга"""
    return {"status": "ok"}
