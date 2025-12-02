from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from faststream import Context
from faststream.nats import NatsRouter

from projects.src.adapters.broker import streams
from projects.src.adapters.broker.cmd import ProjectCmd
from projects.src.adapters.broker.events import ProjectEvents
from projects.src.config.logging import request_id_var
from projects.src.domain.project import ProjectIn, ProjectOut, ProjectsSearchParams, ProjectUpdateCmd
from projects.src.service.project import ProjectService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Projects"], route_class=DishkaRoute)

project_commands = ProjectCmd(service_name="projects", entity_name="Project")
project_events = ProjectEvents(service_name="projects", entity_name="Project")


@broker_router.subscriber(project_commands.create, stream=streams.cmd)
@broker_router.publisher(project_events.created, stream=streams.events)
async def create_project(
        data: ProjectIn,
        project_service: FromDishka[ProjectService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Create a new project. """
    request_id_var.set(cor_id)
    return await project_service.create(data)


@api_router.get("/{project_id}", response_model=ProjectOut)
async def get_project(
        project_id: UUID,
        project_service: FromDishka[ProjectService],
):
    """Get specified project. """
    return await project_service.get(id=project_id)


@api_router.get("", response_model=list[ProjectOut])
async def get_projects_list(
        project_service: FromDishka[ProjectService],
        data: ProjectsSearchParams = Depends(),
):
    """Get all projects by provided fields."""
    return await project_service.list(
        **data.model_dump(exclude_none=True)
    )


@broker_router.subscriber(project_commands.update, stream=streams.cmd)
@broker_router.publisher(project_events.updated, stream=streams.events)
async def update_project(
        update_data: ProjectUpdateCmd,
        project_service: FromDishka[ProjectService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Update specified projects. """
    request_id_var.set(cor_id)
    project = await project_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    return project


@broker_router.subscriber(project_commands.delete, stream=streams.cmd)
@broker_router.publisher(project_events.deleted, stream=streams.events)
async def delete_project(
        project_id: UUID,
        project_service: FromDishka[ProjectService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Delete specified project. """
    request_id_var.set(cor_id)
    await project_service.delete(project_id)
