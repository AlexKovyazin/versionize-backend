from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form

from documents.src.dependencies import get_document_service
from documents.src.domain.schemas.document import DocumentIn, DocumentOut
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
