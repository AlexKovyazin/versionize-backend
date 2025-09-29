import abc
import hashlib
from typing import AsyncGenerator
from uuid import UUID

from documents.src.adapters.orm import OrmDocument
from documents.src.adapters.repository import AbstractDocumentsRepository
from documents.src.adapters.s3 import AbstractS3
from documents.src.config.logging import logger
from documents.src.domain.schemas.document import DocumentIn, DocumentOut, DocumentCreate


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
        doc_path = f"{document_in.section_id}_{md5_hash}"
        await self.s3.put(doc_path, file_content)

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
            doc_path=doc_path
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
            include_fields=(OrmDocument.name, OrmDocument.doc_path,)
        )
        file_stream = self.s3.get(document.doc_path)

        return document.name, file_stream

    async def delete(self, document_id: UUID):
        """ Delete document from S3 and DB. """

        logger.info(f"Deleting document with id {document_id}...")

        document = await self.repository.get(
            id=document_id,
            include_fields=(OrmDocument.doc_path,)
        )
        await self.s3.delete(document.doc_path)
        await self.repository.delete(document_id)

        logger.info(f"Document {document_id} deleted")
