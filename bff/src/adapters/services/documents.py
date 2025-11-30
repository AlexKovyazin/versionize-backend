from uuid import UUID

from bff.src.adapters.broker.cmd import DocumentCmd
from bff.src.adapters.services.base import GenericServiceReadAdapter, GenericServiceWriteAdapter
from bff.src.adapters.services.base import IDocumentsReadServiceAdapter, IDocumentsWriteServiceAdapter
from bff.src.domain.document import DocumentsSearch, DocumentOut, DocumentIn, DocumentUpdate
from bff.src.domain.s3 import S3DownloadResponse, S3UploadResponse


class DocumentsReadServiceAdapter(
    IDocumentsReadServiceAdapter,
    GenericServiceReadAdapter[DocumentsSearch, DocumentOut]
):
    async def get_download_url(self, document_id: UUID, **kwargs) -> S3DownloadResponse:
        response = await self._make_request(
            f"{self.entity_prefix}/{document_id}/get-download-url",
            **kwargs
        )
        return S3DownloadResponse.model_validate(response.json())

    async def get_upload_url(self, document_id: UUID, **kwargs) -> S3UploadResponse:
        response = await self._make_request(
            f"{self.entity_prefix}/{document_id}/get-upload-url",
            **kwargs
        )
        return S3UploadResponse.model_validate(response.json())


class DocumentsWriteServiceAdapter(
    IDocumentsWriteServiceAdapter,
    GenericServiceWriteAdapter[DocumentCmd, DocumentIn, DocumentUpdate]
):
    ...
