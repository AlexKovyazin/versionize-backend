from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi import HTTPException

from documents.src.config.logging import logger
from documents.src.dependencies import get_document_service, get_search_params
from documents.src.domain.document import DocumentIn, DocumentOut, DocumentsSearch, DocumentUpdate
from documents.src.domain.responses import DownloadResponse, UploadResponse
from documents.src.enums import DocumentStatuses
from documents.src.exceptions import FileNotExistError
from documents.src.service.documents_service import DocumentService

router = APIRouter(tags=["Documents"])


@router.post(
    "",
    response_model=DocumentOut,
    status_code=201,
    # just for debugging of auth with identity
    # dependencies=[Depends(get_user)],
    summary="Create a new document in db and upload file to S3.",
    description="""Create a new document in database and upload file to S3.

## Important Notes
When frontend is ready, this endpoint should be rewritten.

**Current Behavior:**
- Creates document metadata in database
- Uploads file directly to S3
- Returns complete document object

**Future Implementation:**
- Use `POST /documents/` for metadata only
- Use `GET /documents/{document_id}/get-upload-url` for file upload (when frontend is ready)

**Flow should be like this:**
- client send document metadata;
- document creates in DB and mark as "not completed" (or something else);
- client get response with all metadata including document_id;
- client make GET request to /{document_id}/get-upload-url and get direct link for S3 uploading;
- client make PUT request to this link with file content;
- after uploading is completed, S3 push message to a queue;
- documents service read this message and mark document as completed;
- if document is not marked as completed for upload link expiring time - responsible user should be notified"""
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
    # TODO: this endpoint should be rewritten to accept only document metadata
    #  as mentioned in description.

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


@router.get("/{document_id}/get-download-url", response_model=DownloadResponse)
async def get_download_url(
        document_id: UUID,
        document_service: DocumentService = Depends(get_document_service),
):
    """ Download document file. """
    try:
        url, filename = await document_service.get_download_url(document_id)
    except FileNotExistError as e:
        raise HTTPException(404, detail=e.args[0])

    return DownloadResponse(
        url=url,  # type: ignore
        filename=filename,
        expires_in=document_service.s3.download_url_expires_in
    )


@router.get("/{document_id}/get-upload-url", response_model=UploadResponse)
async def get_upload_url(
        document_id: UUID,
        document_service: DocumentService = Depends(get_document_service)
):
    url = await document_service.get_upload_url(document_id)
    return UploadResponse(
        url=url,  # type: ignore
        expires_in=document_service.s3.upload_url_expires_in
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


@router.delete("/{document_id}", status_code=204)
async def delete(
        document_id: UUID,
        document_service: DocumentService = Depends(get_document_service),
):
    """Delete a document from S3 and DB."""

    logger.info("Starting of delete request")
    await document_service.delete(document_id)
