from abc import ABC, abstractmethod
from typing import Sequence, TypeVar, Generic, Type
from uuid import UUID

from sqlalchemy import Select, select, update, delete
from sqlalchemy.orm import InstrumentedAttribute, load_only, defer

from documents.src.adapters.orm import Base, OrmDocument
from documents.src.config.logging import logger
from documents.src.service.uow import AbstractUnitOfWork

MODEL = TypeVar("MODEL", bound=Base)
IN_SCHEMA = TypeVar("IN_SCHEMA")


class IGenericRepository(ABC, Generic[MODEL, IN_SCHEMA]):
    def __init__(self, uow: AbstractUnitOfWork, model: Type[MODEL]):
        self.uow = uow
        self.model = model

    @abstractmethod
    async def create(self, entity: IN_SCHEMA) -> MODEL:
        ...

    @abstractmethod
    async def get(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> MODEL:
        ...

    @abstractmethod
    async def get_many(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> list[MODEL]:
        ...

    @abstractmethod
    async def update(self, entity_id: UUID, **kwargs) -> MODEL:
        ...

    @abstractmethod
    async def delete(self, entity_id: UUID) -> None:
        ...


class GenericRepository(IGenericRepository[MODEL, IN_SCHEMA]):
    async def create(self, entity: IN_SCHEMA) -> MODEL:
        logger.info(
            f"Adding new {self.model.__name__} with id {entity.id}...",
            extra=entity.model_dump()
        )
        db_entity = self.model(**entity.model_dump())
        self.uow.session.add(db_entity)
        await self.uow.session.flush()

        logger.info(
            f"New {self.model.__name__} {db_entity.id} added to DB",
            extra=db_entity.to_dict()
        )
        return db_entity

    async def get(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> MODEL:
        """
        Get specified entity from DB.

        @:param include_fields: Sequence of OrmUser fields to include into output object.
        @:param exclude_fields: Sequence of OrmUser fields to exclude from output object.
        @:param kwargs: Filter keywords.

        Example with documents:
        self.get(
          name="Specific document name",
          include_fields=(OrmDocument.section_id, OrmDocument.md5,)
        )
        This call will filter documents by specified name and query only fields of include_fields argument.

        SQL query will be:
        SELECT section_id, md5
          FROM documents
         WHERE name = 'Specific document name'
         ORDER BY created_at DESC
         LIMIT 1
        """

        query = await self._prepare_select(
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            **kwargs
        )
        query_result = await self.uow.session.execute(query)
        db_entity = query_result.scalar_one_or_none()

        return db_entity

    async def get_many(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> list[MODEL]:
        """
        Get specified entities from DB.

        The same as .get, but without limiting.
        """

        query = await self._prepare_select(
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            **kwargs
        )
        query_result = await self.uow.session.execute(query)
        db_entities = query_result.scalars().all()

        return db_entities

    async def update(self, entity_id: UUID, **kwargs) -> MODEL:
        logger.info(
            f"Updating {self.model.__name__} with id {entity_id} in DB...",
            extra=kwargs
        )
        query = (
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**kwargs)
            .returning(self.model)
        )
        result = await self.uow.session.execute(query)
        db_entity = result.scalar_one()

        logger.info(
            f"{self.model.__name__} with id {entity_id} updated in DB",
            extra=db_entity.to_dict()
        )
        return db_entity

    async def delete(self, entity_id: UUID) -> None:
        logger.info(f"Deleting {self.model.__name__} with id {entity_id} from DB...")

        query = delete(self.model).where(self.model.id == entity_id)
        await self.uow.session.execute(query)

        logger.info(f"{self.model.__name__} with id {entity_id} deleted from DB")

    async def _prepare_select(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> Select:
        query = (
            select(self.model)
            .filter_by(**kwargs)
            .order_by(self.model.created_at.desc())
        )
        if include_fields:
            query = query.options(load_only(*include_fields))
        if exclude_fields:
            query = query.options(defer(*exclude_fields))

        return query


class IDocumentsRepository(IGenericRepository, ABC):
    def __init__(self, uow: AbstractUnitOfWork):
        """ Throws model into generic base. """
        super().__init__(uow, OrmDocument)

    @abstractmethod
    async def get_latest(self, section_id: UUID) -> OrmDocument | None:
        ...
