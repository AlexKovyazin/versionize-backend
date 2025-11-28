from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(tags=["Service"])


@router.get("/healthcheck")
async def healthcheck():
    return Response(status_code=200)
