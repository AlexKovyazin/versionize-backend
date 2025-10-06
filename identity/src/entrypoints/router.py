from fastapi import APIRouter

from identity.src.entrypoints.identity import router as identity_router


router = APIRouter()
router.include_router(identity_router, prefix="/identity")
