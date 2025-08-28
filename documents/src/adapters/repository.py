import abc
from uuid import UUID

from sqlalchemy import select

from documents.src.adapters.orm import OrmDocument
from documents.src.domain.schemas.document import DocumentCreate
from documents.src.service.uow import AbstractUnitOfWork


class AbstractDocumentsRepository(abc.ABC):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    @abc.abstractmethod
    async def get_latest(self, section_id: UUID) -> OrmDocument | None:
        ...

    @abc.abstractmethod
    async def create(self, document: DocumentCreate) -> OrmDocument:
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
        """ Creates new document in database. """

        db_document = OrmDocument(**document.model_dump())
        self.uow.session.add(db_document)
        await self.uow.session.flush()

        return db_document
