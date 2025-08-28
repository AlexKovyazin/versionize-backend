from uuid import UUID

from documents.src.adapters.orm import OrmDocument
from documents.src.adapters.repository import AbstractDocumentsRepository
from documents.src.service.uow import AbstractUnitOfWork


class FakeDocumentsRepository(AbstractDocumentsRepository):
    """In-memory fake repository for testing."""

    def __init__(self, uow: AbstractUnitOfWork, documents: list[OrmDocument] = None):
        self.documents = documents or []
        super().__init__(uow)

    async def get_latest(self, section_id: UUID) -> OrmDocument | None:
        docs = [d for d in self.documents if d.section_id == section_id]
        return max(docs, key=lambda x: x.created_at, default=None)

    async def create(self, document_data: dict) -> OrmDocument:
        document = OrmDocument(**document_data)
        self.documents.append(document)
        return document
