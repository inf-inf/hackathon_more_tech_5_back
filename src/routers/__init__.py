from .service import service_router
from .locations import locations_router

api_routers = (
    service_router,
    locations_router,
)
