import abc
import hashlib
from typing import AsyncGenerator
from uuid import UUID

from documents.src.adapters.orm import OrmDocument
from documents.src.adapters.repository import AbstractDocumentsRepository
from documents.src.adapters.s3 import AbstractS3
from documents.src.config.logging import logger
from documents.src.domain.document import DocumentIn, DocumentOut, DocumentCreate
from documents.src.exceptions import FileNotExistError


class AbstractDocumentService(abc.ABC):
    def __init__(
            self,
            repository: AbstractDocumentsRepository,
            s3: AbstractS3
    ):
        self.repository = repository
        self.s3 = s3

    @abc.abstractmethod
    async def create(
            self,
            document_in: DocumentIn,
            file_content: bytes
    ) -> DocumentOut:
        ...

    @abc.abstractmethod
    async def get(self, **kwargs):
        ...

    @abc.abstractmethod
    async def get_many(self, **kwargs):
        ...

    @abc.abstractmethod
    async def download(self, document_id: UUID):
        ...

    @abc.abstractmethod
    async def delete(self, document_id: UUID):
        ...


class DocumentService(AbstractDocumentService):

    async def create(
            self,
            document_in: DocumentIn,
            file_content: bytes,
            raise_variation=False
    ) -> DocumentOut:
        """
        Creates a new document with business logic:
        - MD5 hash generation
        - S3 uploading
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
        md5_hash = hashlib.md5(file_content).hexdigest()
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
            md5=md5_hash,
        )
        created_document = await self.repository.create(document_for_creation)
        created_document = DocumentOut.model_validate(created_document)

        # TODO The S3 call should be removed after using the get-upload-url endpoint.
        await self.s3.put(created_document.id, file_content)

        logger.info(
            f"New document for section {created_document.section_id} created",
            extra=created_document.model_dump()
        )

        return created_document

    async def get(self, **kwargs) -> DocumentOut:
        retrieved_document = await self.repository.get(**kwargs)
        return DocumentOut.model_validate(retrieved_document)

    async def get_many(self, **kwargs) -> list[DocumentOut]:
        retrieved_documents = await self.repository.get_many(**kwargs)
        return [DocumentOut.model_validate(d) for d in retrieved_documents]

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

    async def update(self, document_id: UUID, **kwargs) -> DocumentOut:
        """ Update document attributes in DB. """

        logger.info(f"Updating document {document_id}...")

        updated_document = await self.repository.update(document_id, **kwargs)
        updated_document = DocumentOut.model_validate(updated_document)

        logger.info(f"Document {document_id} updated", extra=updated_document.model_dump())

        return updated_document

    async def delete(self, document_id: UUID):
        """ Delete document from S3 and DB. """

        logger.info(f"Deleting document with id {document_id}...")

        await self.s3.delete(document_id)
        await self.repository.delete(document_id)

        logger.info(f"Document {document_id} deleted")
