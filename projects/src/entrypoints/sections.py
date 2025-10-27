from uuid import UUID

from fastapi import APIRouter, Depends

from projects.src.dependencies import get_section_service
from projects.src.domain.section import SectionIn, SectionOut, SectionsSearch, SectionUpdate
from projects.src.service.section import SectionService

router = APIRouter(tags=["Sections"])


@router.post("", response_model=SectionOut, status_code=201)
async def create(
        data: SectionIn,
        section_service: SectionService = Depends(get_section_service),
):
    """ Create a new section. """
    return await section_service.create(data)


@router.get("/{section_id}", response_model=SectionOut)
async def get(
        section_id: UUID,
        section_service: SectionService = Depends(get_section_service),
):
    """Get specified section. """
    return await section_service.get(id=section_id)


@router.get("", response_model=list[SectionOut])
async def get_many(
        data: SectionsSearch = Depends(),
        section_service: SectionService = Depends(get_section_service),
):
    """Get all sections by provided fields."""
    return await section_service.get_many(
        **data.model_dump(exclude_none=True)
    )


@router.patch("/{section_id}", response_model=SectionOut, status_code=202)
async def update(
        section_id: UUID,
        data: SectionUpdate,
        section_service: SectionService = Depends(get_section_service)
):
    """ Update specified sections. """
    document = await section_service.update(
        section_id,
        **data.model_dump(exclude_none=True)
    )
    return document


@router.delete("/{section_id}", status_code=204)
async def delete(
        section_id: UUID,
        section_service: SectionService = Depends(get_section_service),
):
    """ Delete specified section. """
    await section_service.delete(section_id)
