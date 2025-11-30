from uuid import UUID

from fastapi import APIRouter, Depends

from bff.src.adapters.services.documents import DocumentsReadServiceAdapter, DocumentsWriteServiceAdapter
from bff.src.dependencies import get_documents_read_adapter, get_documents_write_adapter
from bff.src.domain.document import DocumentIn, DocumentOut, DocumentsSearch, DocumentUpdate
from bff.src.domain.s3 import S3DownloadResponse, S3UploadResponse

router = APIRouter(tags=["Documents"])


# TODO Documents.create ## Important Notes
#  When frontend is ready, this endpoint should be rewritten.
#  **Current Behavior:**
#  - Creates document metadata in database
#  - Uploads file directly to S3
#  - Returns complete document object
#  **Future Implementation:**
#  - Use `POST /documents/` for metadata only
#  - Use `GET /documents/{document_id}/get-upload-url` for file upload (when frontend is ready)
#  **Flow should be like this:**
#  - client send document metadata;
#  - document creates in DB and mark as "not completed" (or something else);
#  - client get response with all metadata including document_id;
#  - client make GET request to /{document_id}/get-upload-url and get direct link for S3 uploading;
#  - client make PUT request to this link with file content;
#  - after uploading is completed, S3 push message to a queue (or client make request to callback by himself);
#  - documents service read this message and mark document as completed;
#  - if document is not marked as completed for upload link expiring time - responsible user should be notified"""

@router.post("/documents", status_code=201)
async def create_document(
        data: DocumentIn,
        adapter: DocumentsWriteServiceAdapter = Depends(get_documents_write_adapter)
):
    """ Create a new document. """
    await adapter.create(data)


@router.get("/documents/{document_id}", response_model=DocumentOut)
async def get_document(
        document_id: UUID,
        adapter: DocumentsReadServiceAdapter = Depends(get_documents_read_adapter)
):
    """Get specified document. """
    return await adapter.get(document_id)


@router.get("/documents", response_model=list[DocumentOut])
async def get_many_documents(
        filter_data: DocumentsSearch = Depends(),
        adapter: DocumentsReadServiceAdapter = Depends(get_documents_read_adapter)
):
    """Get all documents by provided fields."""
    return await adapter.list(filter_data)


@router.get("/documents/{document_id}/get-download-url", response_model=S3DownloadResponse)
async def get_download_url(
        document_id: UUID,
        adapter: DocumentsReadServiceAdapter = Depends(get_documents_read_adapter)
):
    """ Get download URL for specified file. """
    return await adapter.get_download_url(document_id)


@router.get("/documents/{document_id}/get-upload-url", response_model=S3UploadResponse)
async def get_upload_url(
        document_id: UUID,
        adapter: DocumentsReadServiceAdapter = Depends(get_documents_read_adapter)
):
    """ Get upload URL for specified file. """
    return await adapter.get_upload_url(document_id)


@router.patch("/documents/{document_id}", status_code=202)
async def update_document(
        document_id: UUID,
        data: DocumentUpdate,
        adapter: DocumentsWriteServiceAdapter = Depends(get_documents_write_adapter)
):
    """ Update specified document. """
    await adapter.update(document_id, data)


@router.delete("/documents/{document_id}", status_code=204)
async def delete_document(
        document_id: UUID,
        adapter: DocumentsWriteServiceAdapter = Depends(get_documents_write_adapter)
):
    """ Delete specified document. """
    await adapter.delete(document_id)
