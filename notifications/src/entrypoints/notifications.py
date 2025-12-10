from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException
from faststream.nats import NatsRouter
from nats.js.api import ConsumerConfig

from notifications.src.adapters.broker import streams
from notifications.src.adapters.broker.cmd import NotificationCmd
from notifications.src.adapters.broker.events import NotificationEvents
from notifications.src.domain.base import EntityDeletedEvent
from notifications.src.domain.notification import NotificationIn, NotificationOut
from notifications.src.domain.notification import NotificationsSearch, NotificationUpdateCmd
from notifications.src.service.notification import NotificationService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Notifications"], route_class=DishkaRoute)

notification_commands = NotificationCmd(service_name="notifications", entity_name="Notification")
notification_events = NotificationEvents(service_name="notifications", entity_name="Notification")


@broker_router.subscriber(
    notification_commands.create,
    stream=streams.cmd,
    queue="notifications-create-workers",
    config=ConsumerConfig(durable_name="notifications-create")
)
@broker_router.publisher(notification_events.created, stream=streams.events)
async def create_notification(
        notification_service: FromDishka[NotificationService],
        data: NotificationIn,
) -> NotificationOut:
    """ Create a new notification. """
    return await notification_service.create(data)


@api_router.get("/{notification_id}", response_model=NotificationOut)
async def get_notification(
        notification_service: FromDishka[NotificationService],
        notification_id: UUID,
) -> NotificationOut:
    """Get specified notification. """

    notification = await notification_service.get(id=notification_id)
    if not notification:
        raise HTTPException(status_code=404)

    return notification


@api_router.get("", response_model=list[NotificationOut])
async def get_notifications_list(
        notification_service: FromDishka[NotificationService],
        data: NotificationsSearch = Depends(),
) -> list[NotificationOut]:
    """Get all notifications by provided fields."""

    return await notification_service.list(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(
    notification_commands.update,
    stream=streams.cmd,
    queue="notifications-update-workers",
    config=ConsumerConfig(durable_name="notifications-update")
)
@broker_router.publisher(notification_events.updated, stream=streams.events)
async def update_notification(
        notification_service: FromDishka[NotificationService],
        update_data: NotificationUpdateCmd,
) -> NotificationOut:
    """ Update specified notifications. """

    notification = await notification_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    if not notification:
        raise Exception("Failed to update non-existent notification")

    return notification


@broker_router.subscriber(
    notification_commands.delete,
    stream=streams.cmd,
    queue="notifications-delete-workers",
    config=ConsumerConfig(durable_name="notifications-delete")
)
@broker_router.publisher(notification_events.deleted, stream=streams.events)
async def delete_notification(
        notification_service: FromDishka[NotificationService],
        notification_id: UUID,
) -> EntityDeletedEvent:
    """ Delete specified notification. """

    deleted_at = await notification_service.delete(notification_id)
    return EntityDeletedEvent(id=notification_id, deleted_at=deleted_at)
