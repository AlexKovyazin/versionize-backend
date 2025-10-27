from fastapi import APIRouter

from projects.src.entrypoints.service import router as service_router
from projects.src.entrypoints.projects import router as project_router
from projects.src.entrypoints.sections import router as section_router
from projects.src.entrypoints.default_sections import router as default_sections_router

router = APIRouter()
router.include_router(service_router, prefix="/service")
router.include_router(project_router, prefix="/projects")
router.include_router(section_router, prefix="/sections")
router.include_router(default_sections_router, prefix="/default_sections")
