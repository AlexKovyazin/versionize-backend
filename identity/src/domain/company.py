import uuid
from datetime import datetime

from pydantic import BaseModel


class Company(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None
    name: str
    phone: str
    email: str
