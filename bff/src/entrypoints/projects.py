from uuid import UUID

from fastapi import APIRouter, Depends

from bff.src.adapters.services.projects import ProjectServiceAdapter
from bff.src.dependencies import get_projects_adapter
from bff.src.domain.project import ProjectOut, ProjectsSearchParams, ProjectIn, ProjectUpdate

router = APIRouter(tags=["Projects"])


@router.post("", status_code=201)
async def create(
        data: ProjectIn,
        projects_adapter: ProjectServiceAdapter = Depends(get_projects_adapter),
):
    """ Create a new project. """

    await projects_adapter.create(data)


@router.get("/{project_id}", response_model=ProjectOut)
async def get(
        project_id: UUID,
        projects_adapter: ProjectServiceAdapter = Depends(get_projects_adapter)
):
    """Get specified project. """
    return await projects_adapter.get(project_id)


@router.get("", response_model=list[ProjectOut])
async def get_many(
        filter_data: ProjectsSearchParams = Depends(),
        projects_adapter: ProjectServiceAdapter = Depends(get_projects_adapter)
):
    """Get all projects by provided fields."""
    return await projects_adapter.get_many(filter_data)

@router.patch("/{project_id}", status_code=202)
async def update(
        data: ProjectUpdate,
        projects_adapter: ProjectServiceAdapter = Depends(get_projects_adapter),
):
    """ Update specified projects. """
    await projects_adapter.update(data)


@router.delete("/{project_id}", status_code=204)
async def delete(
        project_id: UUID,
        projects_adapter: ProjectServiceAdapter = Depends(get_projects_adapter),
):
    """ Delete specified project. """
    await projects_adapter.delete(project_id)
