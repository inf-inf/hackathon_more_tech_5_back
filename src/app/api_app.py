from fastapi import FastAPI

from .lifespan import lifespan
from ..routers import api_routers


class ApiApp(FastAPI):
    def __init__(self, **kwargs):
        super().__init__(
            title="MORE Tech 5.0",
            description="Сервис для подбора оптимального отделения банка, учитывая потребности клиента и доступность "
                        "услуг",
            lifespan=lifespan,
            **kwargs
        )

        for router in api_routers:
            self.include_router(router)
