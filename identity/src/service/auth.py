import abc
from functools import wraps

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer

from identity.src.adapters.keycloak import AbstractKeycloak
from identity.src.adapters.repository import AbstractUsersRepository
from identity.src.config.settings import settings
from identity.src.dependencies import get_authenticated_user
from identity.src.domain.user import User, AuthenticatedUser

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.kc_auth_url,
    tokenUrl=settings.kc_token_url,
    scopes={
        "openid": "OpenID Connect",
    }
)


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


class AbstractAuthService(abc.ABC):
    def __init__(
            self,
            repository: AbstractUsersRepository,
            keycloak: AbstractKeycloak
    ):
        self.repository = repository
        self.keycloak = keycloak

    @abc.abstractmethod
    async def introspect(self, token) -> dict:
        ...

    @abc.abstractmethod
    async def get_or_create_user(
            self,
            authenticated_user: AuthenticatedUser
    ) -> User:
        ...


class AuthService(AbstractAuthService):

    async def introspect(self, token) -> dict:
        return await self.keycloak.introspect(token)

    async def get_or_create_user(
            self,
            authenticated_user: AuthenticatedUser
    ) -> User:
        user = await self.repository.get(id=authenticated_user.id)
        if not user:
            user = await self.repository.create(authenticated_user)

        # because roles are not stored in the database
        # we need to add them from authenticated_user
        user = User.model_validate(user)
        user.roles = authenticated_user.roles

        return User.model_validate(user)
