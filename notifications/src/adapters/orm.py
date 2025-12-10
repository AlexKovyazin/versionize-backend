import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from notifications.src.enums import NotificationType, NotificationStatus, NotificationPriority


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


class OrmNotification(Base):
    __tablename__ = "notifications"

    recipient_id: Mapped[uuid.UUID] = mapped_column(
        index=True, nullable=False,
        comment="Получатель уведомления"
    )
    notification_type: Mapped[NotificationType] = mapped_column(
        index=True, nullable=False,
        comment="Тип уведомления"
    )
    title: Mapped[str] = mapped_column(
        nullable=False,
        comment="Заголовок уведомления"
    )
    body: Mapped[str | None] = mapped_column(
        comment="Текст уведомления"
    )
    status: Mapped[NotificationStatus] = mapped_column(
        index=True, nullable=False, default=NotificationStatus.UNREAD,
        comment="Статус: read|unread|sent|canceled"
    )
    priority: Mapped[NotificationPriority] = mapped_column(
        index=True, nullable=False, default=NotificationPriority.NORMAL,
        comment="Приоритет: low|normal|high|critical"
    )
