import httpx
from fastapi import Depends, HTTPException

from bff.src.adapters.broker.cmd import ProjectCmd
from bff.src.adapters.broker.nats import NatsJS
from bff.src.adapters.services.projects import ProjectsReadServiceAdapter, ProjectsWriteServiceAdapter
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
    return ProjectsReadServiceAdapter()


async def get_projects_write_adapter(
        broker: NatsJS = Depends(get_broker)
) -> ProjectsWriteServiceAdapter:
    """ Returns projects service adapter. """

    return ProjectsWriteServiceAdapter(
        broker,
        ProjectCmd(service_name="projects", entity_name="Project")
    )
