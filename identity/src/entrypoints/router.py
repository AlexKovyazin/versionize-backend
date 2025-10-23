from fastapi import APIRouter

from identity.src.entrypoints.auth import router as auth_router
from identity.src.entrypoints.companies import router as companies_router
from identity.src.entrypoints.service import router as service_router
from identity.src.entrypoints.users import router as users_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth")
router.include_router(service_router, prefix="/service")
router.include_router(users_router, prefix="/users")
router.include_router(companies_router, prefix="/companies")
