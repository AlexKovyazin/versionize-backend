from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(tags=["Identity"])


@router.get("/healthcheck")
async def base_endpoint():
    return Response(status_code=200)
