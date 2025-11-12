from fastapi import APIRouter

from bff.src.entrypoints.service import router as service_router

router = APIRouter()
router.include_router(service_router, prefix="/service")
