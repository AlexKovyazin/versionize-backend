from uuid import UUID

from fastapi import APIRouter, Depends

from bff.src.adapters.projects import ProjectServiceAdapter
from bff.src.dependencies import get_projects_adapter
from bff.src.domain.project import ProjectOut, ProjectsSearchParams

router = APIRouter(tags=["Projects"])


@router.get("/{project_id}", response_model=ProjectOut)
async def get(
        project_id: UUID,
        projects_adapter: ProjectServiceAdapter = Depends(get_projects_adapter)
):
    """Get specified project. """
    return await projects_adapter.get_project(project_id)


@router.get("", response_model=list[ProjectOut])
async def get_many(
        filter_data: ProjectsSearchParams = Depends(),
        projects_adapter: ProjectServiceAdapter = Depends(get_projects_adapter)
):
    """Get all projects by provided fields."""
    return await projects_adapter.get_many_projects(filter_data)
