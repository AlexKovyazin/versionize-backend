import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from bff.src.domain.company import Company
from bff.src.domain.base import BaseValidationMixin
from bff.src.enums import UserProjectRole


class UserBase(BaseModel):
    id: uuid.UUID
    email: str

    model_config = ConfigDict(from_attributes=True)


class AuthenticatedUser(UserBase):
    roles: list[str] = []


class User(AuthenticatedUser):
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    phone: str | None
    company: Company | None
    position: str | None
    project_role: UserProjectRole | None
    last_login: datetime | None
    validated: bool
    created_at: datetime
    updated_at: datetime | None


class UsersSearch(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    phone: str | None = None
    company_id: uuid.UUID | None = None
    position: str | None = None
    validated: bool | None = None


class UserUpdate(BaseValidationMixin, BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    phone: str | None = None
    company_id: uuid.UUID | None = None
    position: str | None = None
