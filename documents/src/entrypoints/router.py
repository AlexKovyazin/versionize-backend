from fastapi import APIRouter

from src.entrypoints.documents import router as documents_router
from src.entrypoints.service import router as service_router

router = APIRouter()
router.include_router(documents_router, prefix="/documents")
router.include_router(service_router, prefix="/documents-service")
