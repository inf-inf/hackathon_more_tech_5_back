from datetime import datetime

from pydantic import Field

from .base import BaseOrmModel


class OfficeHistoryModel(BaseOrmModel):
    dt: datetime
    count_clients: int = Field(alias="countClients")


OfficeHistoryResponse = list[OfficeHistoryModel]
