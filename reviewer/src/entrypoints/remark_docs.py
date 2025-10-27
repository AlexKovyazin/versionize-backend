from uuid import UUID

from fastapi import APIRouter, Depends

from reviewer.src.dependencies import get_remark_doc_service
from reviewer.src.domain.remark_doc import RemarkDocIn, RemarkDocOut, RemarkDocsSearchParams, RemarkDocUpdate
from reviewer.src.service.remark_doc import RemarkDocService

router = APIRouter(tags=["Remark Docs"])


@router.post("", response_model=RemarkDocOut, status_code=201)
async def create(
        data: RemarkDocIn,
        remark_doc_service: RemarkDocService = Depends(get_remark_doc_service),
):
    """ Create a new remark doc. """
    return await remark_doc_service.create(data)


@router.get("/{remark_doc_id}", response_model=RemarkDocOut)
async def get(
        remark_doc_id: UUID,
        remark_doc_service: RemarkDocService = Depends(get_remark_doc_service),
):
    """Get specified remark doc. """
    return await remark_doc_service.get(id=remark_doc_id)


@router.get("", response_model=list[RemarkDocOut])
async def get_many(
        data: RemarkDocsSearchParams = Depends(),
        remark_doc_service: RemarkDocService = Depends(get_remark_doc_service),
):
    """Get all remark docs by provided fields."""
    return await remark_doc_service.get_many(
        **data.model_dump(exclude_none=True)
    )


@router.patch("/{remark_doc_id}", response_model=RemarkDocOut, status_code=202)
async def update(
        remark_doc_id: UUID,
        data: RemarkDocUpdate,
        remark_doc_service: RemarkDocService = Depends(get_remark_doc_service)
):
    """ Update specified remark docs. """
    document = await remark_doc_service.update(
        remark_doc_id,
        **data.model_dump(exclude_none=True)
    )
    return document


@router.delete("/{remark_doc_id}", status_code=204)
async def delete(
        remark_doc_id: UUID,
        remark_doc_service: RemarkDocService = Depends(get_remark_doc_service),
):
    """ Delete specified remark doc. """
    await remark_doc_service.delete(remark_doc_id)
