from fastapi import APIRouter
from faststream.nats import NatsBroker

from projects.src.config.settings import settings
from projects.src.entrypoints.default_sections import router as default_sections_router
from projects.src.entrypoints.projects import api_router as project_api_router
from projects.src.entrypoints.projects import broker_router as project_broker_router
from projects.src.entrypoints.sections import router as section_router
from projects.src.entrypoints.service import router as service_router

router = APIRouter()
broker = NatsBroker(settings.nats_url)

router.include_router(service_router, prefix="/service")
router.include_router(project_api_router, prefix="/projects")
broker.include_router(project_broker_router)
router.include_router(section_router, prefix="/sections")
router.include_router(default_sections_router, prefix="/default_sections")
