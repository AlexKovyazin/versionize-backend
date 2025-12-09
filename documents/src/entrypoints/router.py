from fastapi import APIRouter
from faststream.nats import NatsBroker

from documents.src.config.settings import settings
from documents.src.entrypoints.documents import api_router as documents_api_router
from documents.src.entrypoints.documents import broker_router as documents_broker_router
from documents.src.entrypoints.service import router as service_router
from documents.src.middleware import FSLoggingMiddleware

router = APIRouter()
broker = NatsBroker(
    settings.nats_url,
    middlewares=[FSLoggingMiddleware]
)

router.include_router(service_router, prefix="/service")

router.include_router(documents_api_router, prefix="/documents")
broker.include_router(documents_broker_router)
