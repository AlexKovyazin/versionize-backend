import datetime
from uuid import UUID

from pydantic import BaseModel

from documents.src.enums import DocumentStatuses


class DocumentIn(BaseModel):
    """ Schema for Document creation. """

    section: str
    status: DocumentStatuses | None
    name: str
    note: str | None
    company_id: UUID
    project_id: UUID
    responsible_id: UUID


class DocumentOut(BaseModel):
    """ Schema for Document rendering. """

    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    section: str
    status: DocumentStatuses
    name: str
    version: int
    variation: int
    md5: str
    note: str
    company_id: UUID
    project_id: UUID
    responsible_id: UUID
