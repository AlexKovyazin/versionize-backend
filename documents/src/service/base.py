from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type
from uuid import UUID

from pydantic import BaseModel

from documents.src.adapters.s3 import AbstractS3
from documents.src.domain.document import DocumentIn, DocumentOut
from documents.src.adapters.repositories.base import IGenericRepository

REPO = TypeVar("REPO", bound=IGenericRepository)
IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseModel)
OUT_SCHEMA = TypeVar("OUT_SCHEMA", bound=BaseModel)


class IGenericService(ABC, Generic[REPO, IN_SCHEMA, OUT_SCHEMA]):
    """ Interface of generic service. """

    def __init__(
            self,
            repository: REPO,
            in_schema: Type[IN_SCHEMA],
            out_schema: Type[OUT_SCHEMA]
    ):
        self.repository = repository
        self.in_schema = in_schema
        self.out_schema = out_schema

    @abstractmethod
    async def create(self, entity: IN_SCHEMA, **kwargs) -> IN_SCHEMA:
        ...

    @abstractmethod
    async def get(self, **kwargs) -> OUT_SCHEMA:
        ...

    @abstractmethod
    async def get_many(self, **kwargs) -> list[OUT_SCHEMA]:
        ...

    @abstractmethod
    async def update(self, entity_id: UUID, **kwargs) -> OUT_SCHEMA:
        ...

    @abstractmethod
    async def delete(self, entity_id: UUID) -> None:
        ...


class GenericService(IGenericService[REPO, IN_SCHEMA, OUT_SCHEMA]):
    """ Generic service implementation. """

    async def create(self, entity: IN_SCHEMA, **kwargs) -> OUT_SCHEMA:
        created_entity = await self.repository.create(entity)
        created_entity = self.out_schema.model_validate(created_entity)
        return created_entity

    async def get(self, **kwargs) -> OUT_SCHEMA:
        db_entity = await self.repository.get(**kwargs)
        return self.out_schema.model_validate(db_entity)

    async def get_many(self, **kwargs) -> list[OUT_SCHEMA]:
        db_entity = await self.repository.get_many(**kwargs)
        return [self.out_schema.model_validate(d) for d in db_entity]

    async def update(self, entity_id: UUID, **kwargs) -> OUT_SCHEMA:
        updated_entity = await self.repository.update(entity_id, **kwargs)
        updated_entity = self.out_schema.model_validate(updated_entity)
        return updated_entity

    async def delete(self, entity_id: UUID, **kwargs) -> None:
        await self.repository.delete(entity_id)


class IDocumentService(IGenericService, ABC):
    """ Interface of CompaniesService. """

    def __init__(self, repository: REPO, s3: AbstractS3):
        """ Throws model into generic base. """
        self.s3 = s3
        super().__init__(
            repository=repository,
            in_schema=DocumentIn,
            out_schema=DocumentOut
        )
