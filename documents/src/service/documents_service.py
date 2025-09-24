import abc
import hashlib
from uuid import UUID

from documents.src.adapters.repository import AbstractDocumentsRepository
from documents.src.adapters.s3 import AbstractS3
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
    async def upload(
            self,
            file_path: str,
            file_content: bytes
    ):
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

        md5_hash = hashlib.md5(file_content).hexdigest()
        doc_path = f"{document_in.section_id}_{md5_hash}"
        await self.s3.put(doc_path, file_content)

        latest_document = await self.repository.get_latest(document_in.section_id)
        version = latest_document.version + 1 if latest_document else 1
        variation = 0
        if raise_variation:
            variation = latest_document.variation + 1 if latest_document else 0

        document_for_creation = DocumentCreate(
            **document_in.model_dump(),
            version=version,
            variation=variation,
            md5=md5_hash,
            doc_path=doc_path
        )
        created_document = await self.repository.create(document_for_creation)

        return DocumentOut.model_validate(created_document)

    async def download(self, md5_hash: str):
        """ Download file to S3. """

    async def delete(self, document_id: UUID):
        """ Delete document from db. """
