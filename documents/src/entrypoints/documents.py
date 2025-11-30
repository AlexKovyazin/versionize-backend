from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from faststream import Context
from faststream.nats import NatsRouter

from documents.src.adapters.broker import streams
from documents.src.adapters.broker.cmd import DocumentCmd
from documents.src.adapters.broker.events import DocumentEvents
from documents.src.config.logging import request_id_var
from documents.src.domain.document import DocumentIn, DocumentOut, DocumentsSearch, DocumentUpdateCmd
from documents.src.domain.s3 import S3DownloadResponse, S3UploadResponse
from documents.src.exceptions import FileNotExistError
from documents.src.service.document import DocumentService

broker_router = NatsRouter()
api_router = APIRouter(tags=["Documents"], route_class=DishkaRoute)

document_commands = DocumentCmd(service_name="documents", entity_name="Document")
document_events = DocumentEvents(service_name="documents", entity_name="Document")


@broker_router.subscriber(document_commands.create, stream=streams.cmd)
@broker_router.publisher(document_events.created, stream=streams.events)
async def create(
        data: DocumentIn,
        document_service: FromDishka[DocumentService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Create a new document metadata. """
    request_id_var.set(cor_id)
    return await document_service.create(data)


@api_router.get("/{document_id}", response_model=DocumentOut)
async def get(
        document_id: UUID,
        document_service: FromDishka[DocumentService],
):
    """Get document description without document file."""
    return await document_service.get(id=document_id)


@api_router.get("", response_model=list[DocumentOut])
async def get_many(
        document_service: FromDishka[DocumentService],
        data: DocumentsSearch = Depends(),
):
    """Get all documents descriptions by provided fields."""
    return await document_service.get_many(
        **data.model_dump(exclude_none=True)
    )


@api_router.get("/{document_id}/get-download-url", response_model=S3DownloadResponse)
async def get_download_url(
        document_id: UUID,
        document_service: FromDishka[DocumentService],
):
    """ Get download URL for specified file. """
    try:
        url, filename = await document_service.get_download_url(document_id)
    except FileNotExistError as e:
        raise HTTPException(404, detail=e.args[0])

    return S3DownloadResponse(
        url=url,  # type: ignore
        filename=filename,
        expires_in=document_service.s3.download_url_expires_in
    )


@api_router.get("/{document_id}/get-upload-url", response_model=S3UploadResponse)
async def get_upload_url(
        document_id: UUID,
        document_service: FromDishka[DocumentService],
):
    """ Get upload URL for specified file. """
    url = await document_service.get_upload_url(document_id)
    return S3UploadResponse(
        url=url,  # type: ignore
        expires_in=document_service.s3.upload_url_expires_in
    )


@broker_router.subscriber(document_commands.update, stream=streams.cmd)
@broker_router.publisher(document_events.updated, stream=streams.events)
async def update(
        update_data: DocumentUpdateCmd,
        document_service: FromDishka[DocumentService],
        cor_id: str = Context("message.correlation_id"),
):
    """ Update specified document. """
    request_id_var.set(cor_id)
    document = await document_service.update(
        update_data.id,
        **update_data.data.model_dump(exclude_none=True)
    )
    return document


@broker_router.subscriber(document_commands.delete, stream=streams.cmd)
@broker_router.publisher(document_events.deleted, stream=streams.events)
async def delete(
        document_id: UUID,
        document_service: FromDishka[DocumentService],
        cor_id: str = Context("message.correlation_id"),
):
    """Delete a document from S3 and DB."""
    request_id_var.set(cor_id)
    await document_service.delete(document_id)
