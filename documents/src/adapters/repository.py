from uuid import UUID

from sqlalchemy import select

from documents.src.adapters.orm import OrmDocument
from documents.src.domain.schemas.document import DocumentCreate
from documents.src.service.uow import UnitOfWork
from documents.src.settings import settings


class DocumentsRepository:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

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


def get_documents_repository(uow) -> DocumentsRepository:
    """ Get documents repository or mocked repository for tests. """

    if settings.is_test:
        # TODO: return mocked repo
        pass
    return DocumentsRepository(uow)
