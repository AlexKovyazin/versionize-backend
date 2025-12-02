from typing import AsyncIterable

from dishka import provide, Scope, Provider

from projects.src.adapters.repositories.default_sections import DefaultSectionsRepository
from projects.src.adapters.repositories.projects import ProjectsRepository
from projects.src.adapters.repositories.sections import SectionsRepository
from projects.src.service.default_section import DefaultSectionService
from projects.src.service.project import ProjectService
from projects.src.service.section import SectionService
from projects.src.service.uow import UnitOfWork


class DependencyProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_uow(self) -> AsyncIterable[UnitOfWork]:
        """ Real dependency of UnitOfWork for production. """
        async with UnitOfWork() as uow:
            yield uow

    @provide(scope=Scope.REQUEST)
    async def get_projects_repository(
            self,
            uow: UnitOfWork
    ) -> ProjectsRepository:
        """ Real dependency of ProjectsRepository for production. """
        return ProjectsRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    async def get_sections_repository(
            self,
            uow: UnitOfWork
    ) -> SectionsRepository:
        """ Real dependency of SectionsRepository for production. """
        return SectionsRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    async def get_default_sections_repository(
            self,
            uow: UnitOfWork
    ) -> DefaultSectionsRepository:
        """ Real dependency of DefaultSectionsRepository for production. """
        return DefaultSectionsRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    async def get_project_service(
            self,
            repo: ProjectsRepository,
    ) -> ProjectService:
        """ Real dependency of ProjectService for production. """
        return ProjectService(repo)

    @provide(scope=Scope.REQUEST)
    async def get_section_service(
            self,
            repo: SectionsRepository,
    ) -> SectionService:
        """ Real dependency of SectionService for production. """
        return SectionService(repo)

    @provide(scope=Scope.REQUEST)
    async def get_default_section_service(
            self,
            repo: DefaultSectionsRepository,
    ) -> DefaultSectionService:
        """ Real dependency of DefaultSectionService for production. """
        return DefaultSectionService(repo)
