from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from faststream.nats import NatsRouter
from nats.js.api import ConsumerConfig

from identity.src.adapters.broker import streams
from identity.src.adapters.broker.cmd import UserCmd
from identity.src.adapters.broker.events import UserEvents
from identity.src.domain.base import EntityDeletedEvent
from identity.src.domain.user import User, UsersSearch, UserUpdateCmd
from identity.src.service.user import UserService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Users"], route_class=DishkaRoute)

user_commands = UserCmd(service_name="identity", entity_name="User")
user_events = UserEvents(service_name="identity", entity_name="User")


@api_router.get("/{user_id}", response_model=User)
async def get_user(
        user_service: FromDishka[UserService],
        user_id: UUID,
) -> User:
    """Get specified user. """

    return await user_service.get(id=user_id)


@api_router.get("", response_model=list[User])
async def get_users_list(
        user_service: FromDishka[UserService],
        data: UsersSearch = Depends(),
) -> list[User]:
    """Get all users by provided fields."""

    return await user_service.list(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(
    user_commands.update,
    stream=streams.cmd,
    queue="users-update-workers",
    config=ConsumerConfig(durable_name="users-update")
)
@broker_router.publisher(user_events.updated, stream=streams.events)
async def update_user(
        user_service: FromDishka[UserService],
        update_data: UserUpdateCmd,
) -> User:
    """ Update specified user. """

    user = await user_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    return user


@broker_router.subscriber(
    user_commands.delete,
    stream=streams.cmd,
    queue="users-delete-workers",
    config=ConsumerConfig(durable_name="users-delete")
)
@broker_router.publisher(user_events.deleted, stream=streams.events)
async def delete_user(
        user_service: FromDishka[UserService],
        user_id: UUID,
) -> EntityDeletedEvent:
    """ Delete specified user. """

    deleted_at = await user_service.delete(user_id)
    return EntityDeletedEvent(id=user_id, deleted_at=deleted_at)
