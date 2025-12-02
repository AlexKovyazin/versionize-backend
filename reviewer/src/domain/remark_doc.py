from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from reviewer.src.domain.base import BaseValidationMixin


class RemarkDocIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    version: int
    md5: str
    note: str | None = None
    section_id: UUID
    project_id: UUID


class RemarkDocOut(RemarkDocIn):
    id: UUID
    created_at: datetime
    updated_at: datetime | None


class RemarkDocsSearchParams(BaseModel):
    id: UUID | None = None
    version: int | None = None
    md5: str | None = None
    note: str | None = None
    section_id: UUID | None = None
    project_id: UUID | None = None


class RemarkDocUpdate(BaseValidationMixin, BaseModel):
    note: str | None = None
    section_id: UUID | None = None
    project_id: UUID | None = None


class RemarkDocUpdateCmd(BaseModel):
    id: UUID
    data: RemarkDocUpdate
