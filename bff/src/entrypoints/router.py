from fastapi import APIRouter

from bff.src.entrypoints.service import router as service_router
from bff.src.entrypoints.projects import router as project_router

router = APIRouter()
router.include_router(service_router, prefix="/service")
router.include_router(project_router, prefix="/projects")
