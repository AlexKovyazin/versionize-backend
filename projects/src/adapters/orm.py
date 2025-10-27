from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from projects.src.enums import ProjectType


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


class OrmProject(Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint(
            'company_id', 'code',
            name='uq_company_code',
            comment='Уникальность шифра в рамках организации'
        ),
        UniqueConstraint(
            'company_id', 'name',
            name='uq_company_name',
            comment='Уникальность наименования в рамках организации'
        ),
    )

    code: Mapped[str] = mapped_column(index=True, comment="Шифр")
    name: Mapped[str] = mapped_column(comment="Наименование объекта")
    exp_date: Mapped[datetime | None] = mapped_column(comment="Срок экспертизы")
    next_upload: Mapped[datetime | None] = mapped_column(comment="Крайний срок следующей загрузки в экспертизу")
    pm_id: Mapped[UUID] = mapped_column(comment="ГИП")
    project_type: Mapped[ProjectType] = mapped_column(comment="Тип объекта")
    company_id: Mapped[UUID] = mapped_column(comment="Проектная организация")

    sections: Mapped[list["OrmSection"]] = relationship(
        "OrmSection", back_populates="project"
    )


class OrmSection(Base):
    __tablename__ = "sections"
    __table_args__ = (
        UniqueConstraint(
            "project_id", "name",
            name='uq_project_name',
            comment="Уникальность наименования в рамках проекта"
        ),
        UniqueConstraint(
            "project_id", "abbreviation",
            name='uq_project_abbreviation',
            comment="Уникальность аббревиатуры в рамках проекта"
        )
    )

    name: Mapped[str] = mapped_column(comment="Наименование раздела")
    abbreviation: Mapped[str] = mapped_column(comment="Аббревиатура раздела")
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"), index=True, comment="Объект")
    company_id: Mapped[UUID] = mapped_column(index=True, comment="Ответственная организация")
    responsible_id: Mapped[UUID] = mapped_column(index=True, comment="Ответственный исполнитель")
    expert_id: Mapped[UUID] = mapped_column(index=True, comment="Эксперт")

    project: Mapped["OrmProject"] = relationship(
        "OrmProject", back_populates="sections"
    )


class OrmDefaultSection(Base):
    __tablename__ = "default_sections"
    __table_args__ = (
        UniqueConstraint(
            "project_type", "name",
            name='uq_project_type_name',
            comment="Уникальность наименования в рамках типа объекта"
        ),
        UniqueConstraint(
            "project_type", "abbreviation",
            name='uq_project_type_abbreviation',
            comment="Уникальность аббревиатуры в рамках типа объекта"
        )
    )

    project_type: Mapped[ProjectType] = mapped_column(index=True, comment="Тип объекта")
    name: Mapped[str] = mapped_column(comment="Наименование раздела")
    abbreviation: Mapped[str] = mapped_column(comment="Аббревиатура раздела")
