from fastapi import APIRouter

from documents.src.entrypoints.documents import router as documents_router


router = APIRouter()
router.include_router(documents_router, prefix="/documents")
