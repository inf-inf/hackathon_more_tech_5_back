from contextlib import asynccontextmanager

from .startup import StartupEvent


@asynccontextmanager
async def lifespan(__app):
    """События для запуска/остановки приложения FastAPI

    :param __app: экземпляр приложения FastAPI
    """
    startup_event = StartupEvent()
    startup_event.run()
    yield
