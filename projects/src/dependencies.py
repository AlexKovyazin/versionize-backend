import httpx
from fastapi import Depends, HTTPException

from projects.src.adapters.repositories.projects import ProjectsRepository
from projects.src.adapters.repositories.sections import SectionsRepository, DefaultSectionsRepository
from projects.src.config.settings import settings
from projects.src.domain.user import User
from projects.src.service.auth import oauth2_scheme
from projects.src.service.project import ProjectService
from projects.src.service.section import SectionService, DefaultSectionService
from projects.src.service.uow import UnitOfWork


# TODO удалить после того, как все write действия будут реализованы через брокер

async def get_user(token: str = Depends(oauth2_scheme)):
    """ Real dependency for authenticating of user by identity service. """

    # TODO maybe it should be refactor for using IdentityService class,
    #  not straight call with request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.auth_service_url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise

    return User.model_validate(response.json())


async def get_uow():
    """ Real dependency of UnitOfWork for production. """
    async with UnitOfWork() as uow:
        yield uow


async def get_projects_repository(
        uow=Depends(get_uow)
) -> ProjectsRepository:
    """ Real dependency of ProjectsRepository for production. """
    return ProjectsRepository(uow=uow)


async def get_sections_repository(
        uow=Depends(get_uow)
) -> SectionsRepository:
    """ Real dependency of SectionsRepository for production. """
    return SectionsRepository(uow=uow)


async def get_default_sections_repository(
        uow=Depends(get_uow)
) -> DefaultSectionsRepository:
    """ Real dependency of DefaultSectionsRepository for production. """
    return DefaultSectionsRepository(uow=uow)


async def get_project_service(
        repo=Depends(get_projects_repository),
) -> ProjectService:
    """ Real dependency of ProjectService for production. """
    return ProjectService(repo)


async def get_section_service(
        repo=Depends(get_sections_repository),
) -> SectionService:
    """ Real dependency of SectionService for production. """
    return SectionService(repo)


async def get_default_section_service(
        repo=Depends(get_default_sections_repository),
) -> DefaultSectionService:
    """ Real dependency of DefaultSectionService for production. """
    return DefaultSectionService(repo)
