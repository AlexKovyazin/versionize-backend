from fastapi import APIRouter
from faststream.nats import NatsBroker

from projects.src.config.settings import settings
from projects.src.entrypoints.default_sections import api_router as default_sections_api_router
from projects.src.entrypoints.default_sections import broker_router as default_sections_broker_router
from projects.src.entrypoints.projects import api_router as project_api_router
from projects.src.entrypoints.projects import broker_router as project_broker_router
from projects.src.entrypoints.sections import api_router as section_api_router
from projects.src.entrypoints.sections import broker_router as section_broker_router
from projects.src.entrypoints.service import router as service_router
from projects.src.middleware import FSLoggingMiddleware, RetryMiddleware

router = APIRouter()
broker = NatsBroker(
    settings.nats_url,
    middlewares=[
        FSLoggingMiddleware,
        RetryMiddleware
    ]
)

router.include_router(service_router, prefix="/service")

router.include_router(project_api_router, prefix="/projects")
broker.include_router(project_broker_router)
router.include_router(section_api_router, prefix="/sections")
broker.include_router(section_broker_router)
router.include_router(default_sections_api_router, prefix="/default_sections")
broker.include_router(default_sections_broker_router)
