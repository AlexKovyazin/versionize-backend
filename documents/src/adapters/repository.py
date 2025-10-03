import abc
import uuid
from typing import Sequence
from uuid import UUID

from sqlalchemy import select, delete, Select
from sqlalchemy.orm import load_only, defer, InstrumentedAttribute

from documents.src.adapters.orm import OrmDocument
from documents.src.config.logging import logger
from documents.src.domain.schemas.document import DocumentCreate
from documents.src.service.uow import AbstractUnitOfWork


class AbstractDocumentsRepository(abc.ABC):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    @abc.abstractmethod
    async def create(self, document: DocumentCreate) -> OrmDocument:
        ...

    @abc.abstractmethod
    async def get(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> OrmDocument:
        ...

    @abc.abstractmethod
    async def get_many(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> list[OrmDocument]:
        ...

    @abc.abstractmethod
    async def get_latest(self, section_id: UUID) -> OrmDocument | None:
        ...

    @abc.abstractmethod
    async def delete(self, document_id: UUID) -> OrmDocument:
        ...

    @abc.abstractmethod
    async def _prepare_select(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> Select:
        ...


class DocumentsRepository(AbstractDocumentsRepository):

    async def create(self, document: DocumentCreate) -> OrmDocument:
        """ Creates new document in DB. """

        logger.info(
            f"Adding new document for section {document.section_id} to DB...",
            extra=document.model_dump()
        )
        db_document = OrmDocument(**document.model_dump())
        self.uow.session.add(db_document)
        await self.uow.session.flush()

        logger.info(
            f"New document for section {document.section_id} added to DB",
            extra=db_document.to_dict()
        )
        return db_document

    async def get(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> OrmDocument | None:
        """
        Get specified document from DB.

        @:param include_fields: Sequence of OrmDocument fields to include into output object.
        @:param exclude_fields: Sequence of OrmDocument fields to exclude from output object.
        @:param kwargs: Filter keywords.

        Example:
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
        document = query_result.scalar_one_or_none()

        return document

    async def get_many(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> list[OrmDocument]:
        """
        Get specified documents from DB.

        @:param include_fields: Sequence of OrmDocument fields to include into output object.
        @:param exclude_fields: Sequence of OrmDocument fields to exclude from output object.
        @:param kwargs: Filter keywords.

        The same as .get, but without limiting number of returning objects.

        Example:
        self.get_many(
          name="Specific document name",
          include_fields=(OrmDocument.section_id, OrmDocument.md5,)
        )
        This call will filter documents by specified name and query only fields of include_fields argument.

        SQL query will be:
        SELECT section_id, md5
          FROM documents
         WHERE name = 'Specific document name'
         ORDER BY created_at DESC
        """

        query = await self._prepare_select(
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            **kwargs
        )
        query_result = await self.uow.session.execute(query)
        documents = query_result.scalars().all()

        return documents

    async def get_latest(self, section_id: UUID) -> OrmDocument | None:
        """ Get latest document of specified section if it exists. """

        query = (
            select(OrmDocument)
            .where(OrmDocument.section_id == section_id)
            .order_by(OrmDocument.created_at.desc())
            .limit(1)
        )
        query_result = await self.uow.session.execute(query)
        latest_document = query_result.scalar()

        return latest_document

    async def delete(self, document_id: uuid.UUID) -> None:
        """ Delete document from DB. """

        logger.info(f"Deleting document {document_id} from DB...")

        query = delete(OrmDocument).where(OrmDocument.id == document_id)
        await self.uow.session.execute(query)

        logger.info(f"Document {document_id} successfully deleted from DB")

    async def _prepare_select(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> Select:
        """
        Prepare select query.

        Filter objects by specified kwargs,
        Filter fields to include in output query,
        order results by descending created_at field.
        """

        query = (
            select(OrmDocument)
            .filter_by(**kwargs)
            .order_by(OrmDocument.created_at.desc())
        )
        if include_fields:
            query = query.options(load_only(*include_fields))
        if exclude_fields:
            query = query.options(defer(*exclude_fields))

        return query
