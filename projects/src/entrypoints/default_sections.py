from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from faststream import Context
from faststream.nats import NatsRouter
from nats.js.api import ConsumerConfig

from projects.src.adapters.broker import streams
from projects.src.adapters.broker.cmd import DefaultSectionCmd
from projects.src.adapters.broker.events import DefaultSectionEvents
from projects.src.config.logging import request_id_var
from projects.src.domain.base import EntityDeletedEvent
from projects.src.domain.default_section import DefaultSectionIn, DefaultSectionOut
from projects.src.domain.default_section import DefaultSectionsSearch, DefaultSectionUpdateCmd
from projects.src.service.default_section import DefaultSectionService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Default Sections"], route_class=DishkaRoute)

default_section_commands = DefaultSectionCmd(
    service_name="projects", entity_name="DefaultSection"
)
default_section_events = DefaultSectionEvents(
    service_name="projects", entity_name="DefaultSection"
)


@broker_router.subscriber(
    default_section_commands.create,
    stream=streams.cmd,
    queue="default-sections-create-workers",
    config=ConsumerConfig(durable_name="default-sections-create")
)
@broker_router.publisher(default_section_events.created, stream=streams.events)
async def create_default_section(
        default_section_service: FromDishka[DefaultSectionService],
        data: DefaultSectionIn,
        cor_id: str = Context("message.correlation_id")
) -> DefaultSectionOut:
    """ Create a new default section. """

    request_id_var.set(cor_id)
    return await default_section_service.create(data)


@api_router.get("/{default_section_id}", response_model=DefaultSectionOut)
async def get_default_section(
        default_section_service: FromDishka[DefaultSectionService],
        default_section_id: UUID,
) -> DefaultSectionOut:
    """Get specified default section. """

    return await default_section_service.get(id=default_section_id)


@api_router.get("", response_model=list[DefaultSectionOut])
async def get_default_sections_list(
        default_section_service: FromDishka[DefaultSectionService],
        data: DefaultSectionsSearch = Depends(),
) -> list[DefaultSectionOut]:
    """Get all default sections by provided fields."""

    return await default_section_service.list(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(
    default_section_commands.update,
    stream=streams.cmd,
    queue="default-sections-update-workers",
    config=ConsumerConfig(durable_name="default-sections-update")
)
@broker_router.publisher(default_section_events.updated, stream=streams.events)
async def update_default_section(
        default_section_service: FromDishka[DefaultSectionService],
        update_data: DefaultSectionUpdateCmd,
        cor_id: str = Context("message.correlation_id"),
) -> DefaultSectionOut:
    """ Update specified default sections. """

    request_id_var.set(cor_id)
    default_section = await default_section_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    return default_section


@broker_router.subscriber(
    default_section_commands.delete,
    stream=streams.cmd,
    queue="default-sections-delete-workers",
    config=ConsumerConfig(durable_name="default-sections-delete")
)
@broker_router.publisher(default_section_events.deleted, stream=streams.events)
async def delete_default_section(
        default_section_service: FromDishka[DefaultSectionService],
        default_section_id: UUID,
        cor_id: str = Context("message.correlation_id"),
) -> EntityDeletedEvent:
    """ Delete specified default section. """

    request_id_var.set(cor_id)
    deleted_at = await default_section_service.delete(default_section_id)
    return EntityDeletedEvent(id=default_section_id, deleted_at=deleted_at)
