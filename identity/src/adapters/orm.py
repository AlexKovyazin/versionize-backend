import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from identity.src.enums import UserProjectRole


class Base(DeclarativeBase):
    pass


class BaseMixin:
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


class OrmUser(BaseMixin, Base):
    __tablename__ = "users"

    first_name: Mapped[str | None]
    first_name: Mapped[str | None]
    patronymic: Mapped[str | None]
    email: Mapped[str] = mapped_column(index=True)
    phone: Mapped[str | None]
    position: Mapped[str | None]
    project_role: Mapped[UserProjectRole | None]
    last_login: Mapped[datetime | None]
    company_id: Mapped[str] = mapped_column(
        sa.UUID, sa.ForeignKey("companies.id"), index=True
    )

    company: Mapped["OrmCompany"] = relationship(
        "OrmCompany", back_populates="users"
    )


class OrmCompany(BaseMixin, Base):
    __tablename__ = "companies"

    name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]

    users: Mapped[OrmUser] = relationship(
        "OrmUser", back_populates="company"
    )
