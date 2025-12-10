from uuid import UUID

from fastapi import APIRouter, Depends

from bff.src.adapters.services.notifications import NotificationsReadServiceAdapter, NotificationsWriteServiceAdapter
from bff.src.dependencies import get_notifications_read_adapter, get_notifications_write_adapter
from bff.src.domain.notification import NotificationIn, NotificationUpdate
from bff.src.domain.notification import NotificationOut, NotificationsSearch

router = APIRouter(tags=["Notifications"])


@router.post("/notification", status_code=202)
async def create_notification(
        data: NotificationIn,
        adapter: NotificationsWriteServiceAdapter = Depends(get_notifications_write_adapter)
):
    """ Create a new notification. """
    await adapter.create(data)


@router.get("/notification/{notification_id}", response_model=NotificationOut)
async def get_notification(
        notification_id: UUID,
        adapter: NotificationsReadServiceAdapter = Depends(get_notifications_read_adapter)
):
    """Get specified notification. """
    return await adapter.get(notification_id)


@router.get("/notification", response_model=list[NotificationOut])
async def get_notifications_list(
        filter_data: NotificationsSearch = Depends(),
        adapter: NotificationsReadServiceAdapter = Depends(get_notifications_read_adapter)
):
    """Get all notifications by provided fields."""
    return await adapter.list(filter_data)


@router.patch("/notification/{notification_id}", status_code=202)
async def update_notification(
        notification_id: UUID,
        data: NotificationUpdate,
        adapter: NotificationsWriteServiceAdapter = Depends(get_notifications_write_adapter)
):
    """ Update specified notifications. """
    await adapter.update(notification_id, data)


@router.delete("/notification/{notification_id}", status_code=202)
async def delete_notification(
        notification_id: UUID,
        adapter: NotificationsWriteServiceAdapter = Depends(get_notifications_write_adapter)
):
    """ Delete specified notification. """
    await adapter.delete(notification_id)
