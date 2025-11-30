from fastapi import APIRouter
from faststream.nats import NatsBroker

from identity.src.config.settings import settings
from identity.src.entrypoints.auth import router as auth_router
from identity.src.entrypoints.companies import api_router as companies_api_router
from identity.src.entrypoints.companies import broker_router as companies_broker_router
from identity.src.entrypoints.service import router as service_router
from identity.src.entrypoints.users import api_router as users_api_router
from identity.src.entrypoints.users import broker_router as users_broker_router

router = APIRouter()
broker = NatsBroker(settings.nats_url)

router.include_router(auth_router, prefix="/auth")
router.include_router(service_router, prefix="/service")
router.include_router(users_api_router, prefix="/users")
broker.include_router(users_broker_router)
router.include_router(companies_api_router, prefix="/companies")
broker.include_router(companies_broker_router)
