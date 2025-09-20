from fastapi import APIRouter, Depends

from documents.src.dependencies import get_document_service
from documents.src.domain.schemas.document import DocumentIn, DocumentOut
from documents.src.service.documents_service import DocumentService

router = APIRouter(tags=["Documents"])


@router.post("", status_code=201, response_model=DocumentOut)
async def create_document(
        data: DocumentIn,
        document_service: DocumentService = Depends(get_document_service),
        raise_variation: bool | None = False
):
    """Create a new document in db and upload file to S3."""

    created_document = await document_service.create(data, raise_variation=raise_variation)
    return created_document
