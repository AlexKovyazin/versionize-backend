from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from projects.src.domain.tools import BaseValidationMixin
from projects.src.enums import ProjectType


class SectionIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    abbreviation: str
    project_id: UUID
    company_id: UUID
    responsible_id: UUID | None = None
    expert_id: UUID | None = None


class SectionOut(SectionIn):
    id: UUID
    created_at: datetime
    updated_at: datetime | None


class SectionsSearch(BaseModel):
    id: UUID | None = None
    name: str | None = None
    abbreviation: str | None = None
    project_id: UUID | None = None
    company_id: UUID | None = None
    responsible_id: UUID | None = None
    expert_id: UUID | None = None


class SectionUpdate(BaseValidationMixin, BaseModel):
    name: str | None = None
    abbreviation: str | None = None
    project_id: UUID | None = None
    company_id: UUID | None = None
    responsible_id: UUID | None = None
    expert_id: UUID | None = None


class DefaultSectionIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_type: ProjectType
    name: str
    abbreviation: str


class DefaultSectionOut(DefaultSectionIn):
    id: UUID
    created_at: datetime
    updated_at: datetime | None


class DefaultSectionsSearch(BaseModel):
    id: UUID | None = None
    project_type: ProjectType | None = None
    name: str | None = None
    abbreviation: str | None = None


class DefaultSectionUpdate(BaseValidationMixin, BaseModel):
    project_type: ProjectType | None = None
    name: str | None = None
    abbreviation: str | None = None
