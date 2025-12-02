from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from faststream import Context
from faststream.nats import NatsRouter

from reviewer.src.adapters.broker import streams
from reviewer.src.adapters.broker.cmd import RemarkDocCmd
from reviewer.src.adapters.broker.events import RemarkDocEvents
from reviewer.src.config.logging import request_id_var
from reviewer.src.domain.remark_doc import RemarkDocIn, RemarkDocOut, RemarkDocsSearchParams, RemarkDocUpdateCmd
from reviewer.src.service.remark_doc import RemarkDocService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Remark Docs"], route_class=DishkaRoute)

remark_doc_commands = RemarkDocCmd(service_name="reviewer", entity_name="RemarkDoc")
remark_doc_events = RemarkDocEvents(service_name="reviewer", entity_name="RemarkDoc")


@broker_router.subscriber(remark_doc_commands.create, stream=streams.cmd)
@broker_router.publisher(remark_doc_events.created, stream=streams.events)
async def create_remark_doc(
        data: RemarkDocIn,
        remark_doc_service: FromDishka[RemarkDocService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Create a new remark doc. """
    request_id_var.set(cor_id)
    return await remark_doc_service.create(data)


@api_router.get("/{remark_doc_id}", response_model=RemarkDocOut)
async def get_remark_doc(
        remark_doc_id: UUID,
        remark_doc_service: FromDishka[RemarkDocService],
):
    """Get specified remark doc. """
    return await remark_doc_service.get(id=remark_doc_id)


@api_router.get("", response_model=list[RemarkDocOut])
async def get_remark_docs_list(
        remark_doc_service: FromDishka[RemarkDocService],
        data: RemarkDocsSearchParams = Depends(),
):
    """Get all remark docs by provided fields."""
    return await remark_doc_service.list(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(remark_doc_commands.update, stream=streams.cmd)
@broker_router.publisher(remark_doc_events.updated, stream=streams.events)
async def update_remark_doc(
        update_data: RemarkDocUpdateCmd,
        remark_doc_service: FromDishka[RemarkDocService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Update specified remark docs. """
    request_id_var.set(cor_id)
    remark_doc = await remark_doc_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    return remark_doc


@broker_router.subscriber(remark_doc_commands.delete, stream=streams.cmd)
@broker_router.publisher(remark_doc_events.deleted, stream=streams.events)
async def delete_remark_doc(
        remark_doc_id: UUID,
        remark_doc_service: FromDishka[RemarkDocService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Delete specified remark doc. """
    request_id_var.set(cor_id)
    await remark_doc_service.delete(remark_doc_id)
