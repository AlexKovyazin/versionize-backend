from fastapi import APIRouter, Depends
from fastapi.responses import Response

from reviewer.src.config.settings import settings
from reviewer.src.dependencies import get_user
from reviewer.src.domain.user import User

router = APIRouter(tags=["Service"])


@router.get("/healthcheck")
async def healthcheck():
    return Response(status_code=200)


if settings.debug:
    @router.get("/check-authentication")
    async def check_authentication(user: User = Depends(get_user)):
        return user
