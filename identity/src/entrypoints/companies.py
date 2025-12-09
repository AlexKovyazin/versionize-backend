from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from faststream.nats import NatsRouter
from nats.js.api import ConsumerConfig

from identity.src.adapters.broker import streams
from identity.src.adapters.broker.cmd import CompanyCmd
from identity.src.adapters.broker.events import CompanyEvents
from identity.src.domain.base import EntityDeletedEvent
from identity.src.domain.company import Company, CompanyBase, CompaniesSearch, CompaniesUpdateCmd
from identity.src.service.company import CompaniesService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Companies"], route_class=DishkaRoute)

company_commands = CompanyCmd(service_name="identity", entity_name="Company")
company_events = CompanyEvents(service_name="identity", entity_name="Company")


@broker_router.subscriber(
    company_commands.create,
    stream=streams.cmd,
    queue="companies-create-workers",
    config=ConsumerConfig(durable_name="companies-create")
)
@broker_router.publisher(company_events.created, stream=streams.events)
async def create_company(
        companies_service: FromDishka[CompaniesService],
        data: CompanyBase,
) -> Company:
    """ Create a new company. """
    return await companies_service.create(data)


@api_router.get("/{company_id}", response_model=Company)
async def get_company(
        companies_service: FromDishka[CompaniesService],
        company_id: UUID,
) -> Company:
    """Get specified company. """

    return await companies_service.get(id=company_id)


@api_router.get("", response_model=list[Company])
async def get_companies_list(
        companies_service: FromDishka[CompaniesService],
        data: CompaniesSearch = Depends(),
) -> list[Company]:
    """Get all companies by provided fields."""

    return await companies_service.list(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(
    company_commands.update,
    stream=streams.cmd,
    queue="companies-update-workers",
    config=ConsumerConfig(durable_name="companies-update")
)
@broker_router.publisher(company_events.updated, stream=streams.events)
async def update_company(
        companies_service: FromDishka[CompaniesService],
        update_data: CompaniesUpdateCmd,
) -> Company:
    """ Update specified companies. """

    company = await companies_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    return company


@broker_router.subscriber(
    company_commands.delete,
    stream=streams.cmd,
    queue="companies-delete-workers",
    config=ConsumerConfig(durable_name="companies-delete")
)
@broker_router.publisher(company_events.deleted, stream=streams.events)
async def delete_company(
        companies_service: FromDishka[CompaniesService],
        company_id: UUID,
) -> EntityDeletedEvent:
    """ Delete specified companies. """

    deleted_at = await companies_service.delete(company_id)
    return EntityDeletedEvent(id=company_id, deleted_at=deleted_at)
