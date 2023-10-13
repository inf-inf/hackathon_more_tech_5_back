from pydantic import BaseModel


class HealthcheckResponse(BaseModel):
    """Схема ответа Healthcheck"""
    status: str = "ok"
