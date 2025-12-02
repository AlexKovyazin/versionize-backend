import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from identity.src.domain.base import BaseValidationMixin


class CompanyBase(BaseModel):
    id: uuid.UUID
    name: str
    phone: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class Company(CompanyBase):
    created_at: datetime
    updated_at: datetime | None


class CompaniesSearch(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None


class CompaniesUpdate(
    BaseValidationMixin,
    CompaniesSearch
):
    ...


class CompaniesUpdateCmd(BaseModel):
    id: uuid.UUID
    data: CompaniesUpdate
