import uuid

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from documents.src.enums import DocumentStatuses

Base = declarative_base()


class OrmDocument(Base):
    __tablename__ = "documents"

    id = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4, index=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)
    updated_at = sa.Column(sa.DateTime, onupdate=sa.func.now())
    section = sa.Column(sa.String, nullable=False)
    status = sa.Column(sa.Enum(DocumentStatuses))
    name = sa.Column(sa.String, nullable=False)
    version = sa.Column(sa.Integer, nullable=False)
    variation = sa.Column(sa.Integer, nullable=False)
    md5 = sa.Column(sa.String(32), nullable=False)
    note = sa.Column(sa.String)

    company_id = sa.Column(sa.UUID, nullable=False, index=True)
    project_id = sa.Column(sa.UUID, nullable=False, index=True)
    responsible_id = sa.Column(sa.UUID, nullable=False, index=True)
