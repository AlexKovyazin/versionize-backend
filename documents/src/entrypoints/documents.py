from fastapi import APIRouter, Depends

from documents.src.config import get_uow, get_documents_repository
from documents.src.domain.schemas.document import DocumentIn, DocumentOut
from documents.src.service.documents_service import DocumentService

router = APIRouter(tags=["Documents"])


@router.post("", status_code=201, response_model=DocumentOut)
async def create_document(data: DocumentIn, uow_factory=Depends(get_uow)):
    """ Create a new document in db and upload file to S3. """

    async with uow_factory() as uow:
        documents_repository = get_documents_repository(uow)
        document_service = DocumentService(documents_repository)
        created_document = await document_service.create(data)

    return created_document
