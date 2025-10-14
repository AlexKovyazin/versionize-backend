from fastapi import Depends, HTTPException

from identity.src.adapters.keycloak import Keycloak
from identity.src.adapters.repository import UsersRepository
from identity.src.domain.user import AuthenticatedUser
from identity.src.service.auth import AuthService
from identity.src.service.auth import oauth2_scheme
from identity.src.service.uow import UnitOfWork


async def get_uow():
    """ Real dependency of UnitOfWork for production. """
    async with UnitOfWork() as uow:
        yield uow


async def get_users_repository(uow=Depends(get_uow)) -> UsersRepository:
    """ Real dependency of users repository for production. """
    return UsersRepository(uow)


async def get_keycloak_adapter() -> Keycloak:
    """ Real dependency of keycloak adapter for production. """
    return Keycloak()


async def get_auth_service(
        repo=Depends(get_users_repository),
        keycloak=Depends(get_keycloak_adapter),
) -> AuthService:
    """ Real dependency of AuthService for production. """
    return AuthService(repo, keycloak)


async def get_authenticated_user(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service),
) -> AuthenticatedUser:
    """
    Dependency to get current user from Keycloak token
    """
    try:
        token_info = await auth_service.introspect(token)
        if not token_info.get("active"):
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )
        if not token_info.get("sub"):
            raise HTTPException(
                status_code=401,
                detail="User does not exists"
            )

        realm_access = token_info.get("realm_access", {})
        roles = realm_access.get("roles", [])

        return AuthenticatedUser(
            id=token_info["sub"],
            email=token_info["email"],
            roles=roles
        )

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Authentication failed: {str(e)}"
        )
