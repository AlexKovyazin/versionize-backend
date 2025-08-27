import datetime
from uuid import UUID

from pydantic import BaseModel

from documents.src.enums import DocumentStatuses


class DocumentIn(BaseModel):
    """ Schema for Document creation. """

    name: str
    note: str | None
    status: DocumentStatuses | None
    company_id: UUID
    project_id: UUID
    section_id: UUID
    responsible_id: UUID


class DocumentCreate(DocumentIn):
    """ Schema for Document creation. """

    version: int
    variation: int
    md5: str


class DocumentOut(DocumentCreate):
    """ Schema for Document rendering. """

    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
