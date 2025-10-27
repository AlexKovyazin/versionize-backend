from uuid import UUID

from fastapi import APIRouter, Depends

from projects.src.dependencies import get_project_service
from projects.src.domain.project import ProjectIn, ProjectOut, ProjectsSearchParams, ProjectUpdate
from projects.src.service.project import ProjectService

router = APIRouter(tags=["Projects"])


@router.post("", response_model=ProjectOut, status_code=201)
async def create(
        data: ProjectIn,
        project_service: ProjectService = Depends(get_project_service),
):
    """ Create a new project. """
    return await project_service.create(data)


@router.get("/{project_id}", response_model=ProjectOut)
async def get(
        project_id: UUID,
        project_service: ProjectService = Depends(get_project_service),
):
    """Get specified project. """
    return await project_service.get(id=project_id)


@router.get("", response_model=list[ProjectOut])
async def get_many(
        data: ProjectsSearchParams = Depends(),
        project_service: ProjectService = Depends(get_project_service),
):
    """Get all projects by provided fields."""
    return await project_service.get_many(
        **data.model_dump(exclude_none=True)
    )


@router.patch("/{project_id}", response_model=ProjectOut, status_code=202)
async def update(
        project_id: UUID,
        data: ProjectUpdate,
        project_service: ProjectService = Depends(get_project_service)
):
    """ Update specified projects. """
    document = await project_service.update(
        project_id,
        **data.model_dump(exclude_none=True)
    )
    return document


@router.delete("/{project_id}", status_code=204)
async def delete(
        project_id: UUID,
        project_service: ProjectService = Depends(get_project_service),
):
    """ Delete specified project. """
    await project_service.delete(project_id)
