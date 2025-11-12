from fastapi import APIRouter, Depends
from fastapi.responses import Response

from bff.src.config.settings import settings
from bff.src.dependencies import get_user
from bff.src.domain.user import User

router = APIRouter(tags=["Service"])


@router.get("/healthcheck")
async def healthcheck():
    return Response(status_code=200)


if settings.debug:
    @router.get("/check-authentication")
    async def check_authentication(user: User = Depends(get_user)):
        return user
