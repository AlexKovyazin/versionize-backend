import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from bff.src.domain.company import Company
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