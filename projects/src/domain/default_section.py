from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from projects.src.domain.tools import BaseValidationMixin
from projects.src.enums import ProjectType


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


class DefaultSectionUpdateCmd(BaseValidationMixin, BaseModel):
    id: UUID
    data: DefaultSectionUpdate
