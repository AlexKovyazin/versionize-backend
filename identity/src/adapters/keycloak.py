import abc
from typing import Protocol

from keycloak import KeycloakOpenID

from identity.src.config.settings import settings


class KeycloakClientProtocol(Protocol):
    async def a_introspect(self, token: str) -> dict:
        ...


class AbstractKeycloak(abc.ABC):

    def __init__(self):
        self.client = self._get_client()

    @abc.abstractmethod
    async def introspect(self, token) -> dict:
        ...

    @abc.abstractmethod
    def _get_client(self) -> KeycloakClientProtocol:
        ...


class Keycloak(AbstractKeycloak):

    def _get_client(self):
        return KeycloakOpenID(
            server_url=settings.kc_internal_base_url,
            client_id=settings.kc_client_id,
            realm_name=settings.kc_realm,
            client_secret_key=settings.kc_client_secret.get_secret_value(),
            verify=False if settings.debug else True,
        )

    async def introspect(self, token) -> dict:
        return await self.client.a_introspect(token)
