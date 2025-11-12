import httpx

from bff.src.config.settings import settings
from bff.src.domain.user import User


class AuthService:

    async def get_user(self, token: str) -> User:
        with httpx.AsyncClient() as client:
            response = await client.get(
                settings.AUTH_URL,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()

        return User.model_validate(response.json())
