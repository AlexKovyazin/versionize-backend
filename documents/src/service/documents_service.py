import hashlib
from uuid import UUID

from documents.src.adapters.repository import get_documents_repository
from documents.src.domain.schemas.document import DocumentIn, DocumentOut, DocumentCreate
from documents.src.service.uow import UnitOfWork


class DocumentService:
    def __init__(self, uow: UnitOfWork):
        self.document_repo = get_documents_repository(uow)

    async def create(self, document_in: DocumentIn, file_content: bytes = None) -> DocumentOut:
        """
        Creates a new document with business logic:
        - MD5 hash generation
        - S3 uploading
        - Version management
        - Variation management
        - DB inserting
        """

        md5_hash = hashlib.md5().hexdigest()  # TODO: Generate real MD5 hash
        await self.upload(md5_hash, file_content)

        latest_document = await self.document_repo.get_latest(document_in.section_id)
        version = latest_document.version + 1 if latest_document else 0
        variation = latest_document.variation + 1 if latest_document else 1

        document_for_creation = DocumentCreate(
            **document_in.model_dump(),
            version=version,
            variation=variation,
            md5=md5_hash
        )
        created_document = await self.document_repo.create(document_for_creation)

        return DocumentOut.model_validate(created_document)

    async def upload(self, md5_hash: str, file_content: bytes = None):
        """ Upload file to S3. """

    async def download(self, md5_hash: str):
        """ Download file to S3. """

    async def delete_from_db(self, document_id: UUID):
        """ Delete document from db. """

    async def delete_from_s3(self, md5: str):
        """ Delete document from S3. """
