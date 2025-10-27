from uuid import UUID

from fastapi import APIRouter, Depends

from reviewer.src.dependencies import get_remark_service
from reviewer.src.domain.remark import RemarkIn, RemarkOut, RemarksSearchParams, RemarkUpdate
from reviewer.src.service.remark import RemarkService

router = APIRouter(tags=["Remarks"])


@router.post("", response_model=RemarkOut, status_code=201)
async def create(
        data: RemarkIn,
        remark_service: RemarkService = Depends(get_remark_service),
):
    """ Create a new remark. """
    return await remark_service.create(data)


@router.get("/{remark_id}", response_model=RemarkOut)
async def get(
        remark_id: UUID,
        remark_service: RemarkService = Depends(get_remark_service),
):
    """Get specified remark. """
    return await remark_service.get(id=remark_id)


@router.get("", response_model=list[RemarkOut])
async def get_many(
        data: RemarksSearchParams = Depends(),
        remark_service: RemarkService = Depends(get_remark_service),
):
    """Get all remarks by provided fields."""
    return await remark_service.get_many(
        **data.model_dump(exclude_none=True)
    )


@router.patch("/{remark_id}", response_model=RemarkOut, status_code=202)
async def update(
        remark_id: UUID,
        data: RemarkUpdate,
        remark_service: RemarkService = Depends(get_remark_service)
):
    """ Update specified remarks. """
    document = await remark_service.update(
        remark_id,
        **data.model_dump(exclude_none=True)
    )
    return document


@router.delete("/{remark_id}", status_code=204)
async def delete(
        remark_id: UUID,
        remark_service: RemarkService = Depends(get_remark_service),
):
    """ Delete specified remark. """
    await remark_service.delete(remark_id)
