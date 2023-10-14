from .service import service_router
from .history import history_router
from .locations import locations_router
from .user import user_router

api_routers = (
    service_router,
    locations_router,
    user_router,
    history_router
)
