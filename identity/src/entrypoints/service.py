from fastapi import APIRouter, Depends
from fastapi.responses import Response

from identity.src.config.settings import settings
from identity.src.dependencies import get_authenticated_user, require_roles
from identity.src.domain.user import User, AuthenticatedUser

router = APIRouter(tags=["Service"])


@router.get("/healthcheck")
async def healthcheck():
    """ Health check endpoint. """
    return Response(status_code=200)


if settings.debug:
    @router.get("/check-kc-authentication")
    async def dummy(user: User = Depends(get_authenticated_user)):
        """ Endpoint for checking authentication. """
        return user

    @router.get("/role-protected")
    @require_roles(["admin"])
    async def role_protected(
            authenticated_user: AuthenticatedUser = Depends(get_authenticated_user)
    ):
        """ Endpoint for debug role protected endpoints. """
        return {
            "message": "Access to role-protected granted",
            "user": authenticated_user
        }
