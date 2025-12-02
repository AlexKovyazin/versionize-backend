from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from faststream import Context
from faststream.nats import NatsRouter

from reviewer.src.adapters.broker import streams
from reviewer.src.adapters.broker.cmd import RemarkCmd
from reviewer.src.adapters.broker.events import RemarkEvents
from reviewer.src.config.logging import request_id_var
from reviewer.src.domain.remark import RemarkIn, RemarkOut, RemarksSearchParams, RemarkUpdateCmd
from reviewer.src.service.remark import RemarkService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Remarks"], route_class=DishkaRoute)

remark_commands = RemarkCmd(service_name="reviewer", entity_name="Remark")
remark_events = RemarkEvents(service_name="reviewer", entity_name="Remark")


@broker_router.subscriber(remark_commands.create, stream=streams.cmd)
@broker_router.publisher(remark_events.created, stream=streams.events)
async def create_remark(
        data: RemarkIn,
        remark_service: FromDishka[RemarkService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Create a new remark. """
    request_id_var.set(cor_id)
    return await remark_service.create(data)


@api_router.get("/{remark_id}", response_model=RemarkOut)
async def get_remark(
        remark_id: UUID,
        remark_service: FromDishka[RemarkService],
):
    """Get specified remark. """
    return await remark_service.get(id=remark_id)


@api_router.get("", response_model=list[RemarkOut])
async def get_remarks_list(
        remark_service: FromDishka[RemarkService],
        data: RemarksSearchParams = Depends(),
):
    """Get all remarks by provided fields."""
    return await remark_service.list(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(remark_commands.update, stream=streams.cmd)
@broker_router.publisher(remark_events.updated, stream=streams.events)
async def update_remark(
        update_data: RemarkUpdateCmd,
        remark_service: FromDishka[RemarkService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Update specified remarks. """
    request_id_var.set(cor_id)
    document = await remark_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    return document


@broker_router.subscriber(remark_commands.delete, stream=streams.cmd)
@broker_router.publisher(remark_events.deleted, stream=streams.events)
async def delete_remark(
        remark_id: UUID,
        remark_service: FromDishka[RemarkService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Delete specified remark. """
    request_id_var.set(cor_id)
    await remark_service.delete(remark_id)
