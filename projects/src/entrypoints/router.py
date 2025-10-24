from fastapi import APIRouter

from projects.src.entrypoints.service import router as service_router

router = APIRouter()
router.include_router(service_router, prefix="/projects-service")
