from fastapi import APIRouter

from reviewer.src.entrypoints.service import router as service_router
from reviewer.src.entrypoints.remarks import router as remarks_router
from reviewer.src.entrypoints.remark_docs import router as remark_docs_router

router = APIRouter()
router.include_router(service_router, prefix="/service")
router.include_router(remarks_router, prefix="/remarks")
router.include_router(remark_docs_router, prefix="/remark-docs")
