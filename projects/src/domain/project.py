from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from projects.src.domain.tools import BaseValidationMixin
from projects.src.enums import ProjectType


class ProjectIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    exp_date: datetime | None = None
    next_upload: datetime | None = None
    pm_id: UUID
    project_type: ProjectType
    company_id: UUID


class ProjectOut(ProjectIn):
    id: UUID
    created_at: datetime
    updated_at: datetime | None


class ProjectsSearchParams(BaseModel):
    id: UUID | None = None
    code: str | None = None
    name: str | None = None
    exp_date: datetime | None = None
    next_upload: datetime | None = None
    pm_id: UUID | None = None
    project_type: ProjectType | None = None
    company_id: UUID | None = None


class ProjectUpdate(BaseValidationMixin, BaseModel):
    code: str | None = None
    name: str | None = None
    exp_date: datetime | None = None
    next_upload: datetime | None = None
    pm_id: UUID | None = None
    project_type: ProjectType | None = None
    company_id: UUID | None = None
