import hashlib
from typing import AsyncGenerator
from uuid import UUID

from documents.src.adapters.orm import OrmDocument
from documents.src.adapters.repositories.documents import DocumentsRepository
from documents.src.config.logging import logger
from documents.src.domain.document import DocumentCreate
from documents.src.domain.document import DocumentIn, DocumentOut
from documents.src.exceptions import FileNotExistError
from documents.src.service.base import IDocumentService, GenericService


class DocumentService(
    IDocumentService,
    GenericService[DocumentsRepository, DocumentIn, DocumentOut]
):
    """ DocumentsService implementation. """

    async def create(
            self,
            document_in: DocumentIn,
            raise_variation: bool = False
    ) -> DocumentOut:
        """
        Creates a new document with business logic:
        - Version management
        - Variation management
        - DB inserting

        raise_variation flag used when document is examining by expert.
        If set to True - variation number of new versions will be increased.
        """

        logger.info(
            f"Creating new document for section {document_in.section_id}",
            extra=document_in.model_dump()
        )
        latest_document = await self.repository.get_latest(document_in.section_id)
        version = latest_document.version + 1 if latest_document else 1
        variation = 0
        if raise_variation:
            logger.info(
                f"Raising variation of new document for section {document_in.section_id}",
                extra=document_in.model_dump()
            )
            variation = latest_document.variation + 1 if latest_document else 0

        document_for_creation = DocumentCreate(
            **document_in.model_dump(),
            version=version,
            variation=variation,
        )
        created_document = await self.repository.create(document_for_creation)
        created_document = DocumentOut.model_validate(created_document)

        logger.info(
            f"New document for section {created_document.section_id} created",
            extra=created_document.model_dump()
        )

        return created_document

    async def download(self, document_id: UUID) -> tuple[str, AsyncGenerator]:
        """ Download file from S3. """

        document = await self.repository.get(
            id=document_id,
            include_fields=(OrmDocument.name,)
        )
        file_stream = await self.s3.get_stream(document_id)

        return document.name, file_stream

    async def get_download_url(self, document_id: UUID) -> tuple[str, str]:
        """ Get S3 download url and filename. """

        document = await self.repository.get(
            id=document_id,
            include_fields=[OrmDocument.name]
        )
        if not document:
            raise FileNotExistError("There is no such document in DB")
        url = await self.s3.get_download_url(document_id)

        return url, document.name

    async def get_upload_url(self, document_id: UUID) -> str:
        """  Get S3 upload url. """

        return await self.s3.get_upload_url(document_id)

    async def sync_document_with_file(self, document_id: UUID) -> None:
        """ Sync document with its uploaded file. """

        if not await self.s3.exists(document_id):
            raise FileNotExistError("There is no such document in S3")

        file_stream = await self.s3.get_stream(document_id)
        md5 = hashlib.md5()
        async for chunk in file_stream:
            md5.update(chunk)

        await self.repository.update(
            document_id,
            uploaded=True,
            md5=md5.hexdigest()
        )

    async def delete(self, document_id: UUID, **kwargs):
        """ Delete document from S3 and DB. """

        await self.s3.delete(document_id)
        await self.repository.delete(document_id)
