from typing import Sequence
from uuid import UUID, uuid4
from datetime import datetime
from xml.dom.minidom import Document

from sqlalchemy.orm import InstrumentedAttribute

from documents.src.adapters.orm import OrmDocument
from documents.src.adapters.repository import AbstractDocumentsRepository
from documents.src.domain.document import DocumentCreate
from documents.src.service.uow import AbstractUnitOfWork


class FakeDocumentsRepository(AbstractDocumentsRepository):
    """In-memory fake repository for testing."""

    def __init__(self, uow: AbstractUnitOfWork, documents: list[OrmDocument] = None):
        self.documents = documents or []
        super().__init__(uow)

    async def get_latest(self, section_id: UUID) -> OrmDocument | None:
        docs = [d for d in self.documents if d.section_id == section_id]
        return max(docs, key=lambda x: x.created_at, default=None)

    async def create(self, document: DocumentCreate) -> OrmDocument:
        document = OrmDocument(
            **document.model_dump(),
            id=uuid4(),
            created_at=datetime.now()
        )
        self.documents.append(document)
        return document

    async def get(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> OrmDocument:
        ...

    async def get_many(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> list[OrmDocument]:
        ...

    async def update(
            self,
            document_id: UUID,
            **kwargs
    ) -> OrmDocument:
        ...

    async def delete(
            self,
            document_id: UUID
    ) -> OrmDocument:
        ...
