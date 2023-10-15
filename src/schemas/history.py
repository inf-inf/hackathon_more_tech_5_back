from datetime import datetime
from typing import Annotated

from pydantic import Field

from .base import BaseOrmModel


class OfficeHistoryModel(BaseOrmModel):
    """Загруженность банка в конкретное время"""
    dt: Annotated[
        datetime,
        Field(description="Время, за которое вычисляется количество клиентов в офисе", examples=["2023-10-15 06:00:00"])
    ]
    count_clients: Annotated[
        int,
        Field(alias="countClients", description="Количество клиентов, которое было в офисе во время dt", examples=["4"])
    ]


OfficeHistoryResponse = list[OfficeHistoryModel]
