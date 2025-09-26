import uuid

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from documents.src.enums import DocumentStatuses

Base = declarative_base()


class OrmDocument(Base):
    __tablename__ = "documents"

    id = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4, index=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False, index=True)
    updated_at = sa.Column(sa.DateTime, onupdate=sa.func.now())
    status = sa.Column(sa.Enum(DocumentStatuses), default=DocumentStatuses.NEW, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    version = sa.Column(sa.Integer, nullable=False, comment="Used on expertise")
    variation = sa.Column(sa.Integer, nullable=False, comment="Continuous numbering for every document")
    md5 = sa.Column(sa.String(32), nullable=False, unique=True)
    note = sa.Column(sa.String)
    doc_path = sa.Column(sa.String)

    company_id = sa.Column(sa.UUID, nullable=False, index=True)
    project_id = sa.Column(sa.UUID, nullable=False, index=True)
    section_id = sa.Column(sa.UUID, nullable=False, index=True)
    responsible_id = sa.Column(sa.UUID, nullable=False, index=True)

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
