from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from documents.src.config.logging import logger
from documents.src.dependencies import get_document_service, get_search_params, get_user
from documents.src.domain.document import DocumentIn, DocumentOut, DocumentsSearch, DocumentUpdate
from documents.src.enums import DocumentStatuses
from documents.src.service.documents_service import DocumentService

router = APIRouter(tags=["Documents"])


# TODO for production:
#  - file uploading should be in a separate endpoint of separate service;
#  - it only accept document_id, section_id and file as UploadFile to escape memory issues;
#  - it generates doc_path from section_id and md5 hash;
#  - upload it straight to S3 by chunks;
#  - send msg to a msg queue with doc_path of uploaded file;
#  - documents service get this msg and writes doc_path to corresponding doc.
@router.post(
    "",
    response_model=DocumentOut,
    status_code=201,
    # just for debugging of auth with identity
    dependencies=[Depends(get_user), ]
)
async def create(
        name: str = Form(...),
        note: str | None = Form(...),
        status: DocumentStatuses | None = Form(...),
        company_id: UUID = Form(...),
        project_id: UUID = Form(...),
        section_id: UUID = Form(...),
        responsible_id: UUID = Form(...),
        file: UploadFile = File(...),
        raise_variation: bool | None = False,
        document_service: DocumentService = Depends(get_document_service),
):
    """Create a new document in db and upload file to S3."""

    logger.info("Starting of create request")
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

    logger.info("Starting of get_many request")
    return await document_service.get_many(**data.model_dump(exclude_none=True))


@router.get("/{document_id}", response_model=DocumentOut)
async def get(
        document_id: UUID,
        document_service: DocumentService = Depends(get_document_service),
):
    """Get document description without document file."""

    logger.info("Starting of get request")
    return await document_service.get(id=document_id)


# TODO for production:
#  - file downloading should be in separate service as file uploading
@router.get("/{document_id}/download", response_model=UploadFile)
async def download(
        document_id: UUID,
        document_service: DocumentService = Depends(get_document_service),
):
    """ Download document file. """

    logger.info("Starting of download request")
    filename, stream = await document_service.download(document_id)

    return StreamingResponse(
        stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        }
    )


@router.patch("/{document_id}", response_model=DocumentOut, status_code=202)
async def update(
        document_id: UUID,
        data: DocumentUpdate,
        document_service: DocumentService = Depends(get_document_service)
):
    logger.info("Starting of update request")
    document = await document_service.update(
        document_id,
        **data.model_dump(exclude_none=True)
    )
    return document


# TODO for production:
#  - file reuploading should use the same endpoint that used for base uploading
@router.post("/{document_id}/reupload", status_code=202)
async def reupload(
        document_id: UUID,
        file: UploadFile = File(...),
        document_service: DocumentService = Depends(get_document_service)
):
    logger.info("Starting of reupload request")

    file_content = await file.read()
    await document_service.reupload(document_id, file_content)


@router.delete("/{document_id}", status_code=204)
async def delete(
        document_id: UUID,
        document_service: DocumentService = Depends(get_document_service),
):
    """Delete a document from S3 and DB."""

    logger.info("Starting of delete request")
    await document_service.delete(document_id)
