import httpx
from fastapi import Depends, HTTPException

from reviewer.src.config.settings import settings
from reviewer.src.domain.user import User
from reviewer.src.service.auth import oauth2_scheme
from reviewer.src.service.uow import UnitOfWork


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
