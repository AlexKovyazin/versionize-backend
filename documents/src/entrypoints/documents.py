from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from documents.src.dependencies import get_document_service, get_search_params
from documents.src.domain.schemas.document import DocumentIn, DocumentOut, DocumentsSearch
from documents.src.enums import DocumentStatuses
from documents.src.service.documents_service import DocumentService

router = APIRouter(tags=["Documents"])


@router.post("", status_code=201, response_model=DocumentOut)
async def create_document(
        name: str = Form(...),
        note: str | None = Form(...),
        status: DocumentStatuses | None = Form(...),
        company_id: UUID = Form(...),
        project_id: UUID = Form(...),
        section_id: UUID = Form(...),
        responsible_id: UUID = Form(...),
        file: UploadFile = File(...),
        document_service: DocumentService = Depends(get_document_service),
        raise_variation: bool | None = False
):
    """Create a new document in db and upload file to S3."""

    document_data = DocumentIn(
        name=name,
        note=note,
        status=status,
        company_id=company_id,
        project_id=project_id,
        section_id=section_id,
        responsible_id=responsible_id,
    )
    file_content = await file.read()
    created_document = await document_service.create(
        document_data,
        file_content=file_content,
        raise_variation=raise_variation
    )
    return created_document


@router.get("", response_model=list[DocumentOut])
async def get_many(
        data: DocumentsSearch = Depends(get_search_params),
        document_service: DocumentService = Depends(get_document_service),
):
    """Get all documents descriptions by provided fields."""

    return await document_service.get_many(**data.model_dump(exclude_none=True))


@router.get("/{document_id}", response_model=DocumentOut)
async def get(
        document_id: UUID,
        document_service: DocumentService = Depends(get_document_service),
):
    """Get document description without document file."""

    return await document_service.get(id=document_id)


@router.get("/{document_id}/download", response_model=UploadFile)
async def download(
        document_id: UUID,
        document_service: DocumentService = Depends(get_document_service),
):
    """ Download document file. """

    filename, stream = await document_service.download(document_id)

    return StreamingResponse(
        stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        }
    )


@router.delete("/{document_id}", status_code=204)
async def delete(
        document_id: UUID,
        document_service: DocumentService = Depends(get_document_service),
):
    """Delete a document from S3 and DB."""

    await document_service.delete(document_id)
