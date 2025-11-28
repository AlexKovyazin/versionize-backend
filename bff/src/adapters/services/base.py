from abc import ABC, abstractmethod
from typing import Literal, Generic, TypeVar
from uuid import UUID

import httpx
from nats.js.api import PubAck
from pydantic import BaseModel

from bff.src.adapters.broker.base import IBroker
from bff.src.adapters.broker.cmd import BaseCmd
from bff.src.adapters.broker.nats import Streams
from bff.src.config.logging import request_id_var
from bff.src.config.settings import settings
from bff.src.domain.project import ProjectsSearchParams, ProjectOut
from bff.src.domain.section import DefaultSectionsSearch, DefaultSectionOut

CREATE_SCHEMA = TypeVar("CREATE_SCHEMA", bound=BaseModel)
UPDATE_SCHEMA = TypeVar("UPDATE_SCHEMA", bound=BaseModel)
OUT_SCHEMA = TypeVar("OUT_SCHEMA", bound=BaseModel)
SEARCH_PARAMS = TypeVar("SEARCH_PARAMS", bound=BaseModel)
COMMANDS = TypeVar("COMMANDS", bound=BaseCmd)
HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]


class IServiceAdapter(ABC):
    def __init__(self, service_url: str, entity_prefix: str):
        self.url = service_url
        self.entity_prefix = entity_prefix

    @abstractmethod
    async def _make_request(
            self,
            endpoint: str,
            method: HttpMethod = "GET",
            params: dict = None,
            content: bytes = None,
            data: dict = None,
            json: dict | list = None,
            headers: dict = None,
            cookies: dict = None,
    ) -> httpx.Response:
        """
        Basic wrapper for service calls.

        :param endpoint: endpoint of a specified service
        :param method: HTTP method for the new Request object
        :param params: Query parameters to include in the URL, as a string, dictionary, or sequence of two-tuples.
        :param content: Binary content to include in the body of the request, as bytes or a byte iterator.
        :param data: Form data to include in the body of the request, as a dictionary.
        :param json: A JSON serializable object to include in the body of the request.
        :param headers: Dictionary of HTTP headers to include in the request.
        :param cookies: Dictionary of Cookie items to include in the request.
        :return: response
        """


class IGenericReadServiceAdapter(
    IServiceAdapter,
    Generic[SEARCH_PARAMS, OUT_SCHEMA]
):

    def __init__(
            self,
            service_url: str,
            entity_prefix: str,
            search_params: type[SEARCH_PARAMS],
            out_schema: type[OUT_SCHEMA]
    ):
        self.out_schema = out_schema
        self.search_params = search_params
        super().__init__(service_url, entity_prefix)

    @abstractmethod
    async def get(self, entity_id: UUID) -> OUT_SCHEMA:
        ...

    @abstractmethod
    async def list(self, **kwargs) -> list[OUT_SCHEMA]:
        ...


class IGenericWriteServiceAdapter(
    ABC,
    Generic[COMMANDS, CREATE_SCHEMA, UPDATE_SCHEMA],
):

    def __init__(
            self,
            commands: COMMANDS,
            broker: IBroker
    ):
        self.commands = commands
        self.broker = broker

    @abstractmethod
    async def create(self, entity: CREATE_SCHEMA) -> PubAck:
        ...

    @abstractmethod
    async def update(self, entity_id: UUID, data: UPDATE_SCHEMA) -> PubAck:
        ...

    @abstractmethod
    async def delete(self, entity_id: UUID) -> PubAck:
        ...


class BaseServiceAdapter(IServiceAdapter):
    async def _make_request(
            self,
            endpoint: str,
            method: HttpMethod = "GET",
            params: dict = None,
            content: bytes = None,
            data: dict = None,
            json: dict | list = None,
            headers: dict = None,
            cookies: dict = None,
    ) -> httpx.Response:
        """ Real implementation of cross service calls. """

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.url}/{endpoint}",
                params=params,
                content=content,
                data=data,
                json=json,
                headers=headers,
                cookies=cookies,
            )
            response.raise_for_status()

        return response


class GenericServiceReadAdapter(
    IGenericReadServiceAdapter[SEARCH_PARAMS, OUT_SCHEMA],
    BaseServiceAdapter
):
    async def get(
            self,
            entity_id: UUID,
            **kwargs
    ) -> OUT_SCHEMA:
        """ Get specified entity. """

        response = await self._make_request(
            f"{self.entity_prefix}/{entity_id}",
            **kwargs
        )
        return self.out_schema.model_validate(response.json())

    async def list(
            self,
            search_params: SEARCH_PARAMS,
            **kwargs
    ) -> list[OUT_SCHEMA]:
        """ Get list of entities filtered by search_params. """

        response = await self._make_request(
            self.entity_prefix,
            params=search_params.model_dump(exclude_none=True),
            **kwargs
        )
        return [self.out_schema.model_validate(p) for p in response.json()]


class GenericServiceWriteAdapter(
    IGenericWriteServiceAdapter[COMMANDS, CREATE_SCHEMA, UPDATE_SCHEMA],
):
    async def create(self, entity: CREATE_SCHEMA) -> CREATE_SCHEMA:
        return await self.broker.publish(
            entity,
            self.commands.create,  # type: ignore
            headers={"correlation_id": request_id_var.get()},
            stream=Streams.CMD
        )

    async def update(self, entity_id: UUID, data: UPDATE_SCHEMA) -> OUT_SCHEMA:
        msg = {
            "id": str(entity_id),
            "data": data.model_dump()
        }
        return await self.broker.publish(
            msg,
            self.commands.update,  # type: ignore
            headers={"correlation_id": request_id_var.get()},
            stream=Streams.CMD
        )

    async def delete(self, entity_id: UUID) -> None:
        return await self.broker.publish(
            str(entity_id),
            self.commands.delete,  # type: ignore
            headers={"correlation_id": request_id_var.get()},
            stream=Streams.CMD
        )


class IProjectsReadServiceAdapter(IGenericReadServiceAdapter, ABC):
    def __init__(self):
        super().__init__(
            service_url=settings.projects_read_service_url,
            entity_prefix="projects",
            search_params=ProjectsSearchParams,
            out_schema=ProjectOut
        )


class IProjectsWriteServiceAdapter(IGenericWriteServiceAdapter, ABC):
    def __init__(self, broker: IBroker, commands: BaseCmd):
        super().__init__(
            commands=commands,
            broker=broker
        )


class IDefaultSectionsReadServiceAdapter(IGenericReadServiceAdapter, ABC):
    def __init__(self):
        super().__init__(
            service_url=settings.projects_read_service_url,
            entity_prefix="default_sections",
            search_params=DefaultSectionsSearch,
            out_schema=DefaultSectionOut
        )


class IDefaultSectionsWriteServiceAdapter(IGenericWriteServiceAdapter, ABC):
    def __init__(self, broker: IBroker, commands: BaseCmd):
        super().__init__(
            commands=commands,
            broker=broker
        )
