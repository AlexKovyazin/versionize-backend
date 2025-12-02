from datetime import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(timezone=True),
        server_default=sa.func.now(),
        index=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        sa.TIMESTAMP(timezone=True),
        onupdate=sa.func.now()
    )

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


class OrmRemarkDoc(Base):
    __tablename__ = 'remark_docs'

    version: Mapped[int]
    md5: Mapped[str] = mapped_column(sa.String(32), unique=True)
    note: Mapped[str | None] = mapped_column(comment="Примечание к замечаниям")
    section_id: Mapped[uuid.UUID | None] = mapped_column(index=True)
    project_id: Mapped[uuid.UUID | None] = mapped_column(index=True)

    remarks: Mapped[list["OrmRemark"]] = relationship(
        "OrmRemark", back_populates="remark_doc"
    )


class OrmRemark(Base):
    __tablename__ = 'remarks'

    number: Mapped[int] = mapped_column(comment="Порядковый номер замечания")
    section_id: Mapped[uuid.UUID] = mapped_column(index=True, comment="ID раздела документации")
    expert_id: Mapped[uuid.UUID] = mapped_column(comment="ID эксперта")
    date: Mapped[datetime] = mapped_column(sa.TIMESTAMP(timezone=True), index=True, comment="Дата замечания")
    body: Mapped[str] = mapped_column(comment="Текст замечания")
    link: Mapped[str] = mapped_column(comment="Ссылка на источник замечания в разделе")
    basis: Mapped[str] = mapped_column(comment="Нормативное обоснование замечания")
    remark_doc_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("remark_docs.id"), index=True)

    remark_doc: Mapped["OrmRemarkDoc"] = relationship(
        "OrmRemarkDoc", back_populates="remarks"
    )
