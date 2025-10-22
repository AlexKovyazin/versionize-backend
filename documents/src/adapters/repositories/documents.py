from uuid import UUID

from sqlalchemy import select

from documents.src.adapters.orm import OrmDocument
from documents.src.adapters.repositories.base import AbstractDocumentsRepository, GenericRepository
from documents.src.domain.document import DocumentCreate


class DocumentsRepository(
    AbstractDocumentsRepository,
    GenericRepository[OrmDocument, DocumentCreate]
):
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
