from typing import AsyncIterable

from dishka import provide, Scope, Provider

from identity.src.adapters.keycloak import Keycloak
from identity.src.adapters.repositories.companies import CompaniesRepository
from identity.src.adapters.repositories.users import UsersRepository
from identity.src.service.auth import AuthService
from identity.src.service.company import CompaniesService
from identity.src.service.uow import UnitOfWork
from identity.src.service.user import UserService


class DependencyProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_keycloak_adapter(self) -> Keycloak:
        """ Real dependency of keycloak adapter for production. """
        return Keycloak()

    @provide(scope=Scope.REQUEST)
    async def get_uow(self) -> AsyncIterable[UnitOfWork]:
        """ Real dependency of UnitOfWork for production. """
        async with UnitOfWork() as uow:
            yield uow

    @provide(scope=Scope.REQUEST)
    async def get_companies_repository(
            self,
            uow: UnitOfWork
    ) -> CompaniesRepository:
        """ Real dependency of CompaniesRepository for production. """
        return CompaniesRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    async def get_users_repository(
            self,
            uow: UnitOfWork
    ) -> UsersRepository:
        """ Real dependency of UsersRepository for production. """
        return UsersRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    async def get_companies_service(
            self,
            repo: CompaniesRepository,
    ) -> CompaniesService:
        """ Real dependency of CompaniesService for production. """
        return CompaniesService(repo)

    @provide(scope=Scope.REQUEST)
    async def get_users_service(
            self,
            repo: UsersRepository,
    ) -> UserService:
        """ Real dependency of UserService for production. """
        return UserService(repo)

    @provide(scope=Scope.REQUEST)
    async def get_auth_service(
            self,
            repo: UsersRepository,
            keycloak: Keycloak,
    ) -> AuthService:
        """ Real dependency of AuthService for production. """
        return AuthService(repo, keycloak)
