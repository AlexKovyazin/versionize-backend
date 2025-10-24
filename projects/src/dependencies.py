import httpx
from fastapi import Depends

from projects.src.config.settings import settings
from projects.src.domain.user import User
from projects.src.service.auth import oauth2_scheme


async def get_user(token: str = Depends(oauth2_scheme)):
    """ Real dependency for authenticating of user by identity service. """

    # TODO maybe it should be refactor for using IdentityService class,
    #  not straight call with request
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.auth_service_url,
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()

    return User.model_validate(response.json())
