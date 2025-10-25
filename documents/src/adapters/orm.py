import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from documents.src.enums import DocumentStatuses


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
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


class OrmDocument(Base):
    __tablename__ = "documents"

    status: Mapped[DocumentStatuses] = mapped_column(default=DocumentStatuses.NEW)
    name: Mapped[str]
    version: Mapped[int] = mapped_column(comment="Used on expertise")
    variation: Mapped[int] = mapped_column(comment="Continuous numbering for every document")
    md5: Mapped[str] = mapped_column(sa.String(32), unique=True)
    note: Mapped[str | None]
    # TODO добавь поле, сделай миграцию и реализуй логику томов
    # volume: Mapped[int] = mapped_column(comment="Номер тома")

    company_id: Mapped[uuid.UUID] = mapped_column(index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(index=True)
    section_id: Mapped[uuid.UUID] = mapped_column(index=True)
    responsible_id: Mapped[uuid.UUID] = mapped_column(index=True)
