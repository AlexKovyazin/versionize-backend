from fastapi import APIRouter, Depends
from fastapi.responses import Response, RedirectResponse

from identity.src.config.settings import settings
from identity.src.dependencies import get_authenticated_user, get_auth_service
from identity.src.domain.user import AuthenticatedUser, User
from identity.src.service.auth import AuthService, require_roles

router = APIRouter(tags=["Identity"])


@router.get("/healthcheck")
async def healthcheck():
    return Response(status_code=200)


@router.get("/auth/login/callback")
async def login_callback(
        state: str,
        session_state: str,
        iss: str,
        code: str,
):
    """
    Callback endpoint for auth business logic.

    Note: Auth call makes directly to keycloak auth page.
    This callback is set at keycloak client settings as callback url.
    """

    redirect_url = settings.login_redirect_url
    if settings.debug:
        redirect_url = (
            f"{settings.base_url}/docs/oauth2-redirect?"
            f"state={state}&code={code}&iss={iss}&session_state={session_state}"
        )

    return RedirectResponse(redirect_url)


@router.get("/auth/logout")
async def logout():
    """ Endpoint for logout. """

    # delete bearer from cache
    # and business logic if needed

    return {"logout_url": settings.kc_logout_url}


@router.get("/auth/get-user")
async def get_user(
        authenticated_user: AuthenticatedUser = Depends(get_authenticated_user),
        auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """
    Endpoint for authenticating user by its Bearer token.

    Use flow:
    - frontend calls protected client service endpoint using bearer header;
    - client service (or any) calls identity/auth/get-user through its own dependency;
    - get_authenticated_user dependency calls keycloak through OAuth and get users id and roles;
    - auth service calls db to collect all users data;
    - get_user make User object and return it back to client service;
    - client service do its job and return result to frontend.
    """

    user = await auth_service.resolve_user(authenticated_user)
    return user


# TODO it's temporary endpoint for debug
@router.get("/role-protected")
@require_roles(["admin"])
async def role_protected(
        authenticated_user: AuthenticatedUser = Depends(get_authenticated_user)
):
    return {
        "message": "Access to role-protected granted",
        "user": authenticated_user
    }
