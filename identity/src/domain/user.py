import uuid
from datetime import datetime

from pydantic import BaseModel

from identity.src.domain.company import Company
from identity.src.enums import UserProjectRole


class AuthenticatedUser(BaseModel):
    id: uuid.UUID
    roles: list[str] = []


class User(AuthenticatedUser):
    created_at: datetime
    updated_at: datetime | None

    first_name: str | None
    first_name: str | None
    patronymic: str | None
    email: str
    phone: str | None
    position: str | None
    project_role: UserProjectRole
    last_login: datetime | None
    company: Company
