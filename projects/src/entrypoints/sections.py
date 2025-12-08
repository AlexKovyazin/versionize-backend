from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from faststream import Context
from faststream.nats import NatsRouter
from nats.js.api import ConsumerConfig

from projects.src.adapters.broker import streams
from projects.src.adapters.broker.cmd import SectionCmd
from projects.src.adapters.broker.events import SectionEvents
from projects.src.config.logging import request_id_var
from projects.src.domain.base import EntityDeletedEvent
from projects.src.domain.section import SectionIn, SectionOut, SectionsSearch, SectionUpdateCmd
from projects.src.service.section import SectionService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Sections"], route_class=DishkaRoute)

section_commands = SectionCmd(service_name="projects", entity_name="Section")
section_events = SectionEvents(service_name="projects", entity_name="Section")


@broker_router.subscriber(
    section_commands.create,
    stream=streams.cmd,
    queue="sections-create-workers",
    config=ConsumerConfig(durable_name="sections-create")
)
@broker_router.publisher(section_events.created, stream=streams.events)
async def create_section(
        section_service: FromDishka[SectionService],
        data: SectionIn,
        cor_id: str = Context("message.correlation_id"),
) -> SectionOut:
    """ Create a new section. """

    request_id_var.set(cor_id)
    return await section_service.create(data)


@api_router.get("/{section_id}", response_model=SectionOut)
async def get_section(
        section_service: FromDishka[SectionService],
        section_id: UUID,
) -> SectionOut:
    """Get specified section. """
    return await section_service.get(id=section_id)


@api_router.get("", response_model=list[SectionOut])
async def get_sections_list(
        section_service: FromDishka[SectionService],
        data: SectionsSearch = Depends(),
) -> list[SectionOut]:
    """Get all sections by provided fields."""

    return await section_service.list(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(
    section_commands.update,
    stream=streams.cmd,
    queue="sections-update-workers",
    config=ConsumerConfig(durable_name="sections-update")
)
@broker_router.publisher(section_events.updated, stream=streams.events)
async def update_section(
        section_service: FromDishka[SectionService],
        update_data: SectionUpdateCmd,
        cor_id: str = Context("message.correlation_id"),
) -> SectionOut:
    """ Update specified sections. """

    request_id_var.set(cor_id)
    section = await section_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    return section


@broker_router.subscriber(
    section_commands.delete,
    stream=streams.cmd,
    queue="sections-delete-workers",
    config=ConsumerConfig(durable_name="sections-delete")
)
@broker_router.publisher(section_events.deleted, stream=streams.events)
async def delete_section(
        section_service: FromDishka[SectionService],
        section_id: UUID,
        cor_id: str = Context("message.correlation_id"),
) -> EntityDeletedEvent:
    """ Delete specified section. """

    request_id_var.set(cor_id)
    deleted_at = await section_service.delete(section_id)
    return EntityDeletedEvent(id=section_id, deleted_at=deleted_at)
