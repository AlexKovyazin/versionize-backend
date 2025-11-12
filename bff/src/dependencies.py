import httpx
from fastapi import Depends, HTTPException

from bff.src.adapters.projects import ProjectServiceAdapter
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


async def get_projects_adapter():
    """ Real dependency of ProjectServiceAdapter for production. """
    return ProjectServiceAdapter(settings.projects_service_url)
