from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException
from faststream.nats import NatsRouter
from nats.js.api import ConsumerConfig

from reviewer.src.adapters.broker import streams
from reviewer.src.adapters.broker.cmd import RemarkDocCmd
from reviewer.src.adapters.broker.events import RemarkDocEvents
from reviewer.src.domain.base import EntityDeletedEvent
from reviewer.src.domain.remark_doc import RemarkDocIn, RemarkDocOut, RemarkDocsSearchParams, RemarkDocUpdateCmd
from reviewer.src.service.remark_doc import RemarkDocService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Remark Docs"], route_class=DishkaRoute)

remark_doc_commands = RemarkDocCmd(service_name="reviewer", entity_name="RemarkDoc")
remark_doc_events = RemarkDocEvents(service_name="reviewer", entity_name="RemarkDoc")


@broker_router.subscriber(
    remark_doc_commands.create,
    stream=streams.cmd,
    queue="remark-docs-create-workers",
    config=ConsumerConfig(durable_name="remark-docs-create")
)
@broker_router.publisher(remark_doc_events.created, stream=streams.events)
async def create_remark_doc(
        remark_doc_service: FromDishka[RemarkDocService],
        data: RemarkDocIn,
) -> RemarkDocOut:
    """ Create a new remark doc. """
    return await remark_doc_service.create(data)


@api_router.get("/{remark_doc_id}", response_model=RemarkDocOut)
async def get_remark_doc(
        remark_doc_service: FromDishka[RemarkDocService],
        remark_doc_id: UUID,
) -> RemarkDocOut:
    """Get specified remark doc. """

    remark_doc = await remark_doc_service.get(id=remark_doc_id)
    if not remark_doc:
        raise HTTPException(status_code=404)

    return remark_doc


@api_router.get("", response_model=list[RemarkDocOut])
async def get_remark_docs_list(
        remark_doc_service: FromDishka[RemarkDocService],
        data: RemarkDocsSearchParams = Depends(),
) -> list[RemarkDocOut]:
    """Get all remark docs by provided fields."""

    return await remark_doc_service.list(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(
    remark_doc_commands.update,
    stream=streams.cmd,
    queue="remark-docs-update-workers",
    config=ConsumerConfig(durable_name="remark-docs-update")
)
@broker_router.publisher(remark_doc_events.updated, stream=streams.events)
async def update_remark_doc(
        remark_doc_service: FromDishka[RemarkDocService],
        update_data: RemarkDocUpdateCmd,
) -> RemarkDocOut:
    """ Update specified remark docs. """

    remark_doc = await remark_doc_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    if not remark_doc:
        raise Exception("Failed to update non-existent remark doc")

    return remark_doc


@broker_router.subscriber(
    remark_doc_commands.delete,
    stream=streams.cmd,
    queue="remark-docs-delete-workers",
    config=ConsumerConfig(durable_name="remark-docs-delete")
)
@broker_router.publisher(remark_doc_events.deleted, stream=streams.events)
async def delete_remark_doc(
        remark_doc_service: FromDishka[RemarkDocService],
        remark_doc_id: UUID,
) -> EntityDeletedEvent:
    """ Delete specified remark doc. """

    deleted_at = await remark_doc_service.delete(remark_doc_id)
    return EntityDeletedEvent(id=remark_doc_id, deleted_at=deleted_at)
