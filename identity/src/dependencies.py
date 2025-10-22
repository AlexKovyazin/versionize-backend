from functools import wraps
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from identity.src.adapters.keycloak import Keycloak
from identity.src.adapters.repository import UsersRepository
from identity.src.domain.user import AuthenticatedUser, UsersSearch
from identity.src.service.auth import AuthService
from identity.src.service.auth import oauth2_scheme
from identity.src.service.uow import UnitOfWork
from identity.src.service.user import UserService


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


async def get_user_service(
        repo=Depends(get_users_repository),
):
    """ Real dependency of UserService for production. """
    return UserService(repo)


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


async def get_users_search_params(
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        patronymic: str | None = None,
        phone: str | None = None,
        company_id: UUID | None = None,
        position: str | None = None,
        validated: bool | None = None,
) -> UsersSearch:
    """ Dependency for parsing query results of get requests for getting users. """

    try:
        search_data = UsersSearch(
            email=email,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            phone=phone,
            company_id=company_id,
            position=position,
            validated=validated,
        )
    except ValidationError as e:
        raise RequestValidationError(e.errors())

    return search_data


def require_roles(required_roles: list[str]):
    """ Decorator to require specific roles. """

    def decorator(func):
        @wraps(func)
        async def wrapper(
                *args,
                user: AuthenticatedUser = Depends(get_authenticated_user),
                **kwargs
        ):
            user_roles = set(user.roles)
            required_roles_set = set(required_roles)

            if not user_roles.intersection(required_roles_set):
                raise HTTPException(
                    status_code=403,
                    detail=f"Required roles: {required_roles}"
                )
            return await func(*args, current_user=user, **kwargs)

        return wrapper

    return decorator
