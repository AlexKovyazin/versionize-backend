from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from faststream import Context
from faststream.nats import NatsRouter

from identity.src.adapters.broker import streams
from identity.src.adapters.broker.cmd import CompanyCmd
from identity.src.adapters.broker.events import CompanyEvents
from identity.src.config.logging import request_id_var
from identity.src.domain.company import Company, CompanyBase, CompaniesSearch, CompaniesUpdateCmd
from identity.src.service.company import CompaniesService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Companies"], route_class=DishkaRoute)

company_commands = CompanyCmd(service_name="identity", entity_name="Company")
company_events = CompanyEvents(service_name="identity", entity_name="Company")


@broker_router.subscriber(company_commands.create, stream=streams.cmd)
@broker_router.publisher(company_events.created, stream=streams.events)
async def create(
        data: CompanyBase,
        companies_service: FromDishka[CompaniesService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Create a new company. """
    request_id_var.set(cor_id)
    return await companies_service.create(data)


@api_router.get("/{company_id}", response_model=Company)
async def get(
        company_id: UUID,
        companies_service: FromDishka[CompaniesService],
):
    """Get specified company. """
    return await companies_service.get(id=company_id)


@api_router.get("", response_model=list[Company])
async def get_many(
        companies_service: FromDishka[CompaniesService],
        data: CompaniesSearch = Depends(),
):
    """Get all companies by provided fields."""
    return await companies_service.get_many(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(company_commands.update, stream=streams.cmd)
@broker_router.publisher(company_events.updated, stream=streams.events)
async def update(
        update_data: CompaniesUpdateCmd,
        companies_service: FromDishka[CompaniesService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Update specified companies. """
    request_id_var.set(cor_id)
    document = await companies_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    return document


@broker_router.subscriber(company_commands.delete, stream=streams.cmd)
@broker_router.publisher(company_events.deleted, stream=streams.events)
async def delete(
        company_id: UUID,
        companies_service: FromDishka[CompaniesService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Delete specified companies. """
    request_id_var.set(cor_id)
    await companies_service.delete(company_id)
