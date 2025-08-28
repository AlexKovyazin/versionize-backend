from fastapi import APIRouter, Depends

from documents.src.domain.schemas.document import DocumentIn, DocumentOut
from documents.src.service.documents_service import DocumentService
from documents.src.service.uow import get_uow

router = APIRouter(tags=["Documents"])


@router.post("", status_code=201, response_model=DocumentOut)
async def create_document(data: DocumentIn, uow_factory=Depends(get_uow)):
    """ Create a new document in db and upload file to S3. """

    async with uow_factory() as uow:
        document_service = DocumentService(uow)
        created_document = await document_service.create(data)

    return created_document
