import abc

from fastapi.security import OAuth2AuthorizationCodeBearer

from identity.src.adapters.keycloak import AbstractKeycloak
from identity.src.adapters.repository import AbstractUsersRepository
from identity.src.config.settings import settings
from identity.src.domain.user import User, AuthenticatedUser

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.kc_auth_url,
    tokenUrl=settings.kc_token_url,
    scopes={
        "openid": "OpenID Connect",
    }
)


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
    async def resolve_user(
            self,
            authenticated_user: AuthenticatedUser
    ) -> User:
        ...


class AuthService(AbstractAuthService):

    async def introspect(self, token) -> dict:
        return await self.keycloak.introspect(token)

    async def resolve_user(
            self,
            authenticated_user: AuthenticatedUser
    ) -> User:
        user = await self.repository.get(id=authenticated_user.id)
        if not user:  # TODO keep this logic in auth/login/callback when frontend will be ready
            user = await self.repository.create(authenticated_user)

        # because roles are not stored in the database
        # we need to add them from authenticated_user
        user = User.model_validate(user)
        user.roles = authenticated_user.roles

        return User.model_validate(user)
