from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from reviewer.src.domain.tools import BaseValidationMixin


class RemarkIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    section_id: UUID
    expert_id: UUID
    date: datetime
    body: str
    link: str
    basis: str
    remark_doc_id: UUID


class RemarkOut(RemarkIn):
    id: UUID
    created_at: datetime
    updated_at: datetime | None


class RemarksSearchParams(BaseModel):
    number: int | None = None
    section_id: UUID | None = None
    expert_id: UUID | None = None
    remark_doc_id: UUID | None = None


class RemarkUpdate(BaseValidationMixin, BaseModel):
    number: int | None = None
    section_id: UUID | None = None
    expert_id: UUID | None = None
    date: datetime | None = None
    body: str | None = None
    link: str | None = None
    basis: str | None = None
    remark_doc_id: UUID | None = None