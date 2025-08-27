from uuid import UUID
import hashlib

from sqlalchemy import select

from documents.src.service.uow import UnitOfWork, get_uow
from documents.src.domain.schemas.document import DocumentIn, DocumentOut, DocumentCreate
from documents.src.adapters.orm import OrmDocument
from documents.src.settings import settings


class DocumentsRepository:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_latest(self, section_id: UUID) -> OrmDocument:
        query = (
            select(OrmDocument)
            .where(OrmDocument.section_id == section_id)
            .order_by(OrmDocument.created_at.desc())
            .limit(1)
        )
        query_result = await self.uow.session.execute(query)
        latest_document = query_result.scalar()

        return latest_document

    async def create(self, document: DocumentCreate):
        """ Creates new document in database. """

        db_document = OrmDocument(**document.model_dump())
        await self.uow.session.add(db_document)
        await self.uow.session.commit()
        await self.uow.session.refresh(db_document)

        return db_document


def get_documents_repository(uow) -> DocumentsRepository:
    if settings.IS_TEST:
        # TODO: return mocked repo
        pass
    return DocumentsRepository(uow)
