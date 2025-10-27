from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.now(), index=True)
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=sa.func.now())

    def to_dict(self, exclude: list = None):
        """Convert model instance to dictionary."""

        data = {}
        if exclude is None:
            exclude = []

        for column in self.__table__.columns:
            if column.name not in exclude:
                value = getattr(self, column.name)
                # Convert datetime to ISO format string
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                data[column.name] = value

        return data
