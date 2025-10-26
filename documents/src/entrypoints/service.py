from fastapi import APIRouter, Depends
from fastapi.responses import Response

from documents.src.config.settings import settings
from documents.src.dependencies import get_user
from documents.src.domain.user import User

router = APIRouter(tags=["Service"])


@router.get("/healthcheck")
async def healthcheck():
    return Response(status_code=200)


if settings.debug:
    @router.get("/check-authentication")
    async def dummy(user: User = Depends(get_user)):
        return user
