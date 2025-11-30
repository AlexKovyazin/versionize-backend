import httpx
from fastapi import Depends, HTTPException

from bff.src.adapters.broker.cmd import ProjectCmd
from bff.src.adapters.broker.nats import NatsJS
from bff.src.adapters.services.identity import CompaniesReadServiceAdapter, CompaniesWriteServiceAdapter
from bff.src.adapters.services.identity import UsersReadServiceAdapter, UsersWriteServiceAdapter
from bff.src.adapters.services.projects import DefaultSectionsReadServiceAdapter, DefaultSectionsWriteServiceAdapter
from bff.src.adapters.services.projects import ProjectsReadServiceAdapter, ProjectsWriteServiceAdapter
from bff.src.adapters.services.projects import SectionsReadServiceAdapter, SectionsWriteServiceAdapter
from bff.src.config.settings import settings
from bff.src.domain.user import User
from bff.src.service.auth import oauth2_scheme


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


async def get_broker() -> NatsJS:
    """ Returns broker adapter. """
    return NatsJS()


async def get_projects_read_adapter() -> ProjectsReadServiceAdapter:
    """ Returns projects read service adapter. """
    return ProjectsReadServiceAdapter()


async def get_projects_write_adapter(
        broker: NatsJS = Depends(get_broker)
) -> ProjectsWriteServiceAdapter:
    """ Returns projects write service adapter. """

    return ProjectsWriteServiceAdapter(
        broker,
        ProjectCmd(service_name="projects", entity_name="Project")
    )


async def get_default_sections_read_adapter() -> DefaultSectionsReadServiceAdapter:
    """ Returns default sections read service adapter. """
    return DefaultSectionsReadServiceAdapter()


async def get_default_sections_write_adapter(
        broker: NatsJS = Depends(get_broker)
) -> DefaultSectionsWriteServiceAdapter:
    """ Returns default sections write service adapter. """

    return DefaultSectionsWriteServiceAdapter(
        broker,
        ProjectCmd(service_name="projects", entity_name="DefaultSection")
    )


async def get_sections_read_adapter() -> SectionsReadServiceAdapter:
    """ Returns sections read service adapter. """
    return SectionsReadServiceAdapter()


async def get_sections_write_adapter(
        broker: NatsJS = Depends(get_broker)
) -> SectionsWriteServiceAdapter:
    """ Returns sections write service adapter. """

    return SectionsWriteServiceAdapter(
        broker,
        ProjectCmd(service_name="projects", entity_name="Section")
    )


async def get_users_read_adapter() -> UsersReadServiceAdapter:
    """ Returns users read service adapter. """
    return UsersReadServiceAdapter()


async def get_users_write_adapter(
        broker: NatsJS = Depends(get_broker)
) -> UsersWriteServiceAdapter:
    """ Returns users write service adapter. """

    return UsersWriteServiceAdapter(
        broker,
        ProjectCmd(service_name="identity", entity_name="User")
    )


async def get_companies_read_adapter() -> CompaniesReadServiceAdapter:
    """ Returns companies read service adapter. """
    return CompaniesReadServiceAdapter()


async def get_companies_write_adapter(
        broker: NatsJS = Depends(get_broker)
) -> CompaniesWriteServiceAdapter:
    """ Returns companies write service adapter. """

    return CompaniesWriteServiceAdapter(
        broker,
        ProjectCmd(service_name="identity", entity_name="Company")
    )
