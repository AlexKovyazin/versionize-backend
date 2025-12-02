from uuid import UUID

from fastapi import APIRouter, Depends

from bff.src.adapters.services.projects import DefaultSectionsReadServiceAdapter, DefaultSectionsWriteServiceAdapter
from bff.src.adapters.services.projects import ProjectsReadServiceAdapter, ProjectsWriteServiceAdapter
from bff.src.adapters.services.projects import SectionsReadServiceAdapter, SectionsWriteServiceAdapter
from bff.src.dependencies import get_default_sections_read_adapter, get_default_sections_write_adapter
from bff.src.dependencies import get_projects_read_adapter, get_projects_write_adapter
from bff.src.dependencies import get_sections_read_adapter, get_sections_write_adapter
from bff.src.domain.project import ProjectIn, ProjectUpdate
from bff.src.domain.project import ProjectOut, ProjectsSearchParams
from bff.src.domain.section import DefaultSectionIn, DefaultSectionUpdate
from bff.src.domain.section import DefaultSectionOut, DefaultSectionsSearch
from bff.src.domain.section import SectionIn, SectionUpdate
from bff.src.domain.section import SectionOut, SectionsSearch

router = APIRouter(tags=["Projects"])


@router.post("/project", status_code=202)
async def create_project(
        data: ProjectIn,
        adapter: ProjectsWriteServiceAdapter = Depends(get_projects_write_adapter)
):
    """ Create a new project. """
    await adapter.create(data)


@router.get("/project/{project_id}", response_model=ProjectOut)
async def get_project(
        project_id: UUID,
        adapter: ProjectsReadServiceAdapter = Depends(get_projects_read_adapter)
):
    """Get specified project. """
    return await adapter.get(project_id)


@router.get("/project", response_model=list[ProjectOut])
async def get_projects_list(
        filter_data: ProjectsSearchParams = Depends(),
        adapter: ProjectsReadServiceAdapter = Depends(get_projects_read_adapter)
):
    """Get all projects by provided fields."""
    return await adapter.list(filter_data)


@router.patch("/project/{project_id}", status_code=202)
async def update_project(
        project_id: UUID,
        data: ProjectUpdate,
        adapter: ProjectsWriteServiceAdapter = Depends(get_projects_write_adapter)
):
    """ Update specified projects. """
    await adapter.update(project_id, data)


@router.delete("/project/{project_id}", status_code=202)
async def delete_project(
        project_id: UUID,
        adapter: ProjectsWriteServiceAdapter = Depends(get_projects_write_adapter)
):
    """ Delete specified project. """
    await adapter.delete(project_id)


@router.post("/default-section", status_code=202)
async def create_default_section(
        data: DefaultSectionIn,
        adapter: DefaultSectionsWriteServiceAdapter = Depends(get_default_sections_write_adapter)
):
    """ Create a new default section. """
    await adapter.create(data)


@router.get("/default-section/{default_section_id}", response_model=DefaultSectionOut)
async def get_default_section(
        default_section_id: UUID,
        adapter: DefaultSectionsReadServiceAdapter = Depends(get_default_sections_read_adapter)
):
    """Get specified default section. """
    return await adapter.get(default_section_id)


@router.get("/default-section", response_model=list[DefaultSectionOut])
async def get_default_sections_list(
        filter_data: DefaultSectionsSearch = Depends(),
        adapter: DefaultSectionsReadServiceAdapter = Depends(get_default_sections_read_adapter)
):
    """Get all default sections by provided fields."""
    return await adapter.list(filter_data)


@router.patch("/default-section/{default_section_id}", status_code=202)
async def update_default_section(
        default_section_id: UUID,
        data: DefaultSectionUpdate,
        adapter: DefaultSectionsWriteServiceAdapter = Depends(get_default_sections_write_adapter)
):
    """ Update specified default section. """
    await adapter.update(default_section_id, data)


@router.delete("/default-section/{default_section_id}", status_code=202)
async def delete_default_section(
        default_section_id: UUID,
        adapter: DefaultSectionsWriteServiceAdapter = Depends(get_default_sections_write_adapter)
):
    """ Delete specified default section. """
    await adapter.delete(default_section_id)


@router.post("/section", status_code=202)
async def create_section(
        data: SectionIn,
        adapter: SectionsWriteServiceAdapter = Depends(get_sections_write_adapter)
):
    """ Create a new section. """
    await adapter.create(data)


@router.get("/section/{section_id}", response_model=SectionOut)
async def get_section(
        section_id: UUID,
        adapter: SectionsReadServiceAdapter = Depends(get_sections_read_adapter)
):
    """Get specified section. """
    return await adapter.get(section_id)


@router.get("/section", response_model=list[SectionOut])
async def get_sections_list(
        filter_data: SectionsSearch = Depends(),
        adapter: SectionsReadServiceAdapter = Depends(get_sections_read_adapter)
):
    """Get all sections by provided fields."""
    return await adapter.list(filter_data)


@router.patch("/section/{section_id}", status_code=202)
async def update_section(
        section_id: UUID,
        data: SectionUpdate,
        adapter: SectionsWriteServiceAdapter = Depends(get_sections_write_adapter)
):
    """ Update specified section. """
    await adapter.update(section_id, data)


@router.delete("/section/{section_id}", status_code=202)
async def delete_section(
        section_id: UUID,
        adapter: SectionsWriteServiceAdapter = Depends(get_sections_write_adapter)
):
    """ Delete specified section. """
    await adapter.delete(section_id)
