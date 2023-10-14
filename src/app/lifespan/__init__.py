from contextlib import asynccontextmanager

from sqlalchemy.orm import Session

from .startup import StartupEvent
from src.database.base import engine


@asynccontextmanager
async def lifespan(__app):
    """События для запуска/остановки приложения FastAPI

    :param __app: экземпляр приложения FastAPI
    """
    with Session(engine) as session:
        startup_event = StartupEvent(session)
        startup_event.run()
        session.commit()
    yield
