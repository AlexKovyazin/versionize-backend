from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from notifications.src.domain.base import BaseValidationMixin
from notifications.src.enums import NotificationType, NotificationStatus, NotificationPriority


class NotificationIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recipient_id: UUID
    notification_type: NotificationType
    title: str
    body: str | None = None
    # status: NotificationStatus | None = None
    priority: NotificationPriority | None = None


class NotificationOut(NotificationIn):
    id: UUID
    created_at: datetime
    updated_at: datetime | None
    status: NotificationStatus | None


class NotificationsSearch(BaseModel):
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    status: NotificationStatus | None = None
    recipient_id: UUID | None = None
    title: str | None = None
    notification_type: NotificationType
    priority: NotificationPriority | None = None


class NotificationUpdate(BaseValidationMixin, BaseModel):
    recipient_id: UUID | None = None
    title: str | None = None
    body: str | None = None
    status: NotificationStatus | None = None
    priority: NotificationPriority | None = None
    notification_type: NotificationType | None = None


class NotificationUpdateCmd(BaseValidationMixin, BaseModel):
    id: UUID
    data: NotificationUpdate
