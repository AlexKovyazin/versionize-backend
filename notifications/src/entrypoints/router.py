from fastapi import APIRouter
from faststream.nats import NatsBroker

from notifications.src.config.settings import settings
from notifications.src.entrypoints.notifications import api_router as notification_api_router
from notifications.src.entrypoints.notifications import broker_router as notification_broker_router
from notifications.src.entrypoints.service import router as service_router
from notifications.src.middleware import FSLoggingMiddleware, RetryMiddleware

router = APIRouter()
broker = NatsBroker(
    settings.nats_url,
    middlewares=[
        FSLoggingMiddleware,
        RetryMiddleware
    ]
)

router.include_router(service_router, prefix="/service")

router.include_router(notification_api_router, prefix="/notifications")
broker.include_router(notification_broker_router)
