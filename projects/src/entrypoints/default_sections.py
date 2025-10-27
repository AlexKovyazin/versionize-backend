from uuid import UUID

from fastapi import APIRouter, Depends

from projects.src.dependencies import get_default_section_service
from projects.src.domain.section import DefaultSectionIn, DefaultSectionOut, DefaultSectionsSearch, DefaultSectionUpdate
from projects.src.service.section import DefaultSectionService

router = APIRouter(tags=["Default Sections"])


@router.post("", response_model=DefaultSectionOut, status_code=201)
async def create(
        data: DefaultSectionIn,
        default_section_service: DefaultSectionService = Depends(get_default_section_service),
):
    """ Create a new section. """
    return await default_section_service.create(data)


@router.get("/{default_section_id}", response_model=DefaultSectionOut)
async def get(
        default_section_id: UUID,
        default_section_service: DefaultSectionService = Depends(get_default_section_service),
):
    """Get specified section. """
    return await default_section_service.get(id=default_section_id)


@router.get("", response_model=list[DefaultSectionOut])
async def get_many(
        data: DefaultSectionsSearch = Depends(),
        default_section_service: DefaultSectionService = Depends(get_default_section_service),
):
    """Get all sections by provided fields."""
    return await default_section_service.get_many(
        **data.model_dump(exclude_none=True)
    )


@router.patch("/{default_section_id}", response_model=DefaultSectionOut, status_code=202)
async def update(
        default_section_id: UUID,
        data: DefaultSectionUpdate,
        default_section_service: DefaultSectionService = Depends(get_default_section_service)
):
    """ Update specified sections. """
    document = await default_section_service.update(
        default_section_id,
        **data.model_dump(exclude_none=True)
    )
    return document


@router.delete("/{default_section_id}", status_code=204)
async def delete(
        default_section_id: UUID,
        default_section_service: DefaultSectionService = Depends(get_default_section_service),
):
    """ Delete specified section. """
    await default_section_service.delete(default_section_id)
