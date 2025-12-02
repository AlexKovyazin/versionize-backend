from uuid import UUID

from fastapi import APIRouter, Depends

from bff.src.adapters.services.documents import DocumentsReadServiceAdapter, DocumentsWriteServiceAdapter
from bff.src.dependencies import get_documents_read_adapter, get_documents_write_adapter
from bff.src.domain.document import DocumentIn, DocumentOut, DocumentsSearch, DocumentUpdate
from bff.src.domain.s3 import S3DownloadResponse, S3UploadResponse

router = APIRouter(tags=["Documents"])


@router.post("/documents", status_code=201)
async def create_document(
        data: DocumentIn,
        adapter: DocumentsWriteServiceAdapter = Depends(get_documents_write_adapter)
):
    """
    Create a new document in DB.

    **Flow of full document creation:**
    - Client send document metadata to **/documents**;
    - Document creates in DB and mark as "uploaded=false, md5=NULL";
    - Client make GET request to **/documents/{document_id}**
      To get full document metadata with calculated fields including document_id;
    - Client make GET request to **/documents/{document_id}/get-upload-url** and get presigned url for S3 uploading;
    - Client make PUT request to presigned url with file content as octet-stream;
    - After uploading is completed, client make request to **/documents/{document_id}/uploaded**;
    - BFF send command to documents service to sync document metadata with uploaded file;
      - Documents service read this message;
      - Verify that file exists;
      - Get its md5;
      - Set md5 and mark document as uploaded in DB.
    - If document is not marked as uploaded for presigned url expiring time - responsible user should be notified.
    """
    await adapter.create(data)


@router.get("/documents/{document_id}", response_model=DocumentOut)
async def get_document(
        document_id: UUID,
        adapter: DocumentsReadServiceAdapter = Depends(get_documents_read_adapter)
):
    """Get specified document. """
    return await adapter.get(document_id)


@router.get("/documents", response_model=list[DocumentOut])
async def get_documents_list(
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


@router.post("/documents/{document_id}/uploaded")
async def upload_callback(
        document_id: UUID,
        adapter: DocumentsWriteServiceAdapter = Depends(get_documents_write_adapter)
):
    """
    Upload callback for specified file.

    Called by client after document file uploading.
    """
    return await adapter.sync_document_file(document_id)


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
