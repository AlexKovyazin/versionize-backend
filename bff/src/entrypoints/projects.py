from uuid import UUID

from fastapi import APIRouter, Depends

from bff.src.adapters.services.projects import ProjectsReadServiceAdapter, ProjectsWriteServiceAdapter
from bff.src.dependencies import get_projects_read_adapter, get_projects_write_adapter
from bff.src.domain.project import ProjectOut, ProjectsSearchParams, ProjectIn, ProjectUpdate

router = APIRouter(tags=["Projects"])


@router.post("", status_code=201)
async def create(
        data: ProjectIn,
        adapter: ProjectsWriteServiceAdapter = Depends(get_projects_write_adapter)
):
    """ Create a new project. """

    await adapter.create(data)


@router.get("/{project_id}", response_model=ProjectOut)
async def get(
        project_id: UUID,
        adapter: ProjectsReadServiceAdapter = Depends(get_projects_read_adapter)
):
    """Get specified project. """
    return await adapter.get(project_id)


@router.get("", response_model=list[ProjectOut])
async def get_many(
        filter_data: ProjectsSearchParams = Depends(),
        adapter: ProjectsReadServiceAdapter = Depends(get_projects_read_adapter)
):
    """Get all projects by provided fields."""
    return await adapter.list(filter_data)

@router.patch("/{project_id}", status_code=202)
async def update(
        project_id: UUID,
        data: ProjectUpdate,
        adapter: ProjectsWriteServiceAdapter = Depends(get_projects_write_adapter)
):
    """ Update specified projects. """
    await adapter.update(project_id, data)


@router.delete("/{project_id}", status_code=204)
async def delete(
        project_id: UUID,
        adapter: ProjectsWriteServiceAdapter = Depends(get_projects_write_adapter)
):
    """ Delete specified project. """
    await adapter.delete(project_id)
