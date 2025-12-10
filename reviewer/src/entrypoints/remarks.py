from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException
from faststream.nats import NatsRouter
from nats.js.api import ConsumerConfig

from reviewer.src.adapters.broker import streams
from reviewer.src.adapters.broker.cmd import RemarkCmd
from reviewer.src.adapters.broker.events import RemarkEvents
from reviewer.src.domain.base import EntityDeletedEvent
from reviewer.src.domain.remark import RemarkIn, RemarkOut, RemarksSearchParams, RemarkUpdateCmd
from reviewer.src.service.remark import RemarkService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Remarks"], route_class=DishkaRoute)

remark_commands = RemarkCmd(service_name="reviewer", entity_name="Remark")
remark_events = RemarkEvents(service_name="reviewer", entity_name="Remark")


@broker_router.subscriber(
    remark_commands.create,
    stream=streams.cmd,
    queue="remarks-create-workers",
    config=ConsumerConfig(durable_name="remarks-create")
)
@broker_router.publisher(remark_events.created, stream=streams.events)
async def create_remark(
        remark_service: FromDishka[RemarkService],
        data: RemarkIn,
) -> RemarkOut:
    """ Create a new remark. """
    return await remark_service.create(data)


@api_router.get("/{remark_id}", response_model=RemarkOut)
async def get_remark(
        remark_service: FromDishka[RemarkService],
        remark_id: UUID,
) -> RemarkOut:
    """Get specified remark. """

    remark = await remark_service.get(id=remark_id)
    if not remark:
        raise HTTPException(status_code=404)

    return await remark_service.get(id=remark_id)


@api_router.get("", response_model=list[RemarkOut])
async def get_remarks_list(
        remark_service: FromDishka[RemarkService],
        data: RemarksSearchParams = Depends(),
) -> list[RemarkOut]:
    """Get all remarks by provided fields."""

    return await remark_service.list(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(
    remark_commands.update,
    stream=streams.cmd,
    queue="remarks-update-workers",
    config=ConsumerConfig(durable_name="remarks-update")
)
@broker_router.publisher(remark_events.updated, stream=streams.events)
async def update_remark(
        remark_service: FromDishka[RemarkService],
        update_data: RemarkUpdateCmd,
) -> RemarkOut:
    """ Update specified remarks. """

    remark = await remark_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    if not remark:
        raise Exception("Failed to update non-existent remark")
    return remark


@broker_router.subscriber(
    remark_commands.delete,
    stream=streams.cmd,
    queue="remarks-delete-workers",
    config=ConsumerConfig(durable_name="remarks-delete")
)
@broker_router.publisher(remark_events.deleted, stream=streams.events)
async def delete_remark(
        remark_service: FromDishka[RemarkService],
        remark_id: UUID,
) -> EntityDeletedEvent:
    """ Delete specified remark. """

    deleted_at = await remark_service.delete(remark_id)
    return EntityDeletedEvent(id=remark_id, deleted_at=deleted_at)
