import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator

from documents.src.enums import DocumentStatuses


class DocumentIn(BaseModel):
    """ Schema for Document creation. """

    model_config = ConfigDict(from_attributes=True)

    name: str
    note: str | None
    status: DocumentStatuses | None = None
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
    updated_at: datetime.datetime | None


class BaseValidationMixin:

    @model_validator(mode="after")
    def validate_at_least_one_field(cls, values):
        provided_fields = [
            field_name for field_name, field_value in values
            if field_value is not None
        ]

        if not provided_fields:
            raise ValueError("At least one field must be provided")

        return values


class DocumentsSearch(BaseModel):
    id: UUID | None = None
    company_id: UUID | None = None
    project_id: UUID | None = None
    section_id: UUID | None = None
    responsible_id: UUID | None = None


class DocumentUpdate(BaseValidationMixin, BaseModel):
    name: str | None = None
    note: str | None = None
    status: DocumentStatuses | None = None
    project_id: UUID | None = None
    section_id: UUID | None = None
    responsible_id: UUID | None = None
