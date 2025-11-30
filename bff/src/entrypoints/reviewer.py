from uuid import UUID

from fastapi import APIRouter, Depends

from bff.src.adapters.services.reviewer import RemarkDocsReadServiceAdapter, RemarkDocsWriteServiceAdapter
from bff.src.adapters.services.reviewer import RemarksReadServiceAdapter, RemarksWriteServiceAdapter
from bff.src.dependencies import get_remark_docs_read_adapter, get_remark_docs_write_adapter
from bff.src.dependencies import get_remarks_read_adapter, get_remarks_write_adapter
from bff.src.domain.remark import RemarkIn, RemarksSearch, RemarkOut, RemarkUpdate
from bff.src.domain.remark_doc import RemarkDocIn, RemarkDocsSearch, RemarkDocOut, RemarkDocUpdate

router = APIRouter(tags=["Reviewer"])


@router.post("/remarks", status_code=201)
async def create_remark(
        data: RemarkIn,
        adapter: RemarksWriteServiceAdapter = Depends(get_remarks_write_adapter)
):
    """ Create a new remark. """
    await adapter.create(data)


@router.get("/remarks/{remark_id}", response_model=RemarkOut)
async def get_remark(
        remark_id: UUID,
        adapter: RemarksReadServiceAdapter = Depends(get_remarks_read_adapter),
):
    """Get specified remark. """
    return await adapter.get(remark_id)


@router.get("/remarks", response_model=list[RemarkOut])
async def get_many_remarks(
        filter_data: RemarksSearch = Depends(),
        adapter: RemarksReadServiceAdapter = Depends(get_remarks_read_adapter),
):
    """Get all remarks by provided fields."""
    return await adapter.list(filter_data)


@router.patch("/remarks/{remark_id}", status_code=202)
async def update_remark(
        remark_id: UUID,
        data: RemarkUpdate,
        adapter: RemarksWriteServiceAdapter = Depends(get_remarks_write_adapter)
):
    """ Update specified remark. """
    await adapter.update(remark_id, data)


@router.delete("/remarks/{remark_id}", status_code=204)
async def delete_remark(
        remark_id: UUID,
        adapter: RemarksWriteServiceAdapter = Depends(get_remarks_write_adapter)
):
    """ Delete specified remark. """
    await adapter.delete(remark_id)


@router.post("/remark-docs", status_code=201)
async def create_remark_doc(
        data: RemarkDocIn,
        adapter: RemarkDocsWriteServiceAdapter = Depends(get_remark_docs_write_adapter)
):
    """ Create a new remark_doc. """
    await adapter.create(data)


@router.get("/remark-docs/{remark_doc_id}", response_model=RemarkDocOut)
async def get_remark_doc(
        remark_doc_id: UUID,
        adapter: RemarkDocsReadServiceAdapter = Depends(get_remark_docs_read_adapter)
):
    """Get specified remark_doc. """
    return await adapter.get(remark_doc_id)


@router.get("/remark-docs", response_model=list[RemarkDocOut])
async def get_many_remark_docs(
        filter_data: RemarkDocsSearch = Depends(),
        adapter: RemarkDocsReadServiceAdapter = Depends(get_remark_docs_read_adapter)
):
    """Get all remark_docs by provided fields."""
    return await adapter.list(filter_data)


@router.patch("/remark-docs/{remark_doc_id}", status_code=202)
async def update_remark_doc(
        remark_doc_id: UUID,
        data: RemarkDocUpdate,
        adapter: RemarkDocsWriteServiceAdapter = Depends(get_remark_docs_write_adapter)
):
    """ Update specified remark_doc. """
    await adapter.update(remark_doc_id, data)


@router.delete("/remark-docs/{remark_doc_id}", status_code=204)
async def delete_remark_doc(
        remark_doc_id: UUID,
        adapter: RemarkDocsWriteServiceAdapter = Depends(get_remark_docs_write_adapter)
):
    """ Delete specified remark_doc. """
    await adapter.delete(remark_doc_id)
