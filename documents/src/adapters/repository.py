import abc
import uuid
from typing import Sequence
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import load_only, defer, InstrumentedAttribute

from documents.src.adapters.orm import OrmDocument
from documents.src.config.logging import logger
from documents.src.domain.schemas.document import DocumentCreate
from documents.src.service.uow import AbstractUnitOfWork


class AbstractDocumentsRepository(abc.ABC):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    @abc.abstractmethod
    async def get(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> OrmDocument:
        ...

    @abc.abstractmethod
    async def get_latest(self, section_id: UUID) -> OrmDocument | None:
        ...

    @abc.abstractmethod
    async def create(self, document: DocumentCreate) -> OrmDocument:
        ...

    @abc.abstractmethod
    async def delete(self, document_id: UUID) -> OrmDocument:
        ...


class DocumentsRepository(AbstractDocumentsRepository):

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
    ) -> OrmDocument:
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
        """

        query = (
            select(OrmDocument)
            .filter_by(**kwargs)
        )
        if include_fields:
            query = query.options(load_only(*include_fields))
        if exclude_fields:
            query = query.options(defer(*exclude_fields))

        query_result = await self.uow.session.execute(query)
        db_document = query_result.scalar_one_or_none()

        return db_document

    async def delete(self, document_id: uuid.UUID) -> None:
        """ Delete document from DB. """

        logger.info(f"Deleting document {document_id} from DB...")

        query = delete(OrmDocument).where(OrmDocument.id == document_id)
        await self.uow.session.execute(query)

        logger.info(f"Document {document_id} successfully deleted from DB")
