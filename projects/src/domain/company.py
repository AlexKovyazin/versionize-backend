import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Company(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None
    name: str
    phone: str
    email: str

    model_config = ConfigDict(from_attributes=True)
