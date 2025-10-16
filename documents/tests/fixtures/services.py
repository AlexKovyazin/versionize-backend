from documents.src.domain.document import DocumentIn, DocumentOut
from documents.src.service.documents_service import AbstractDocumentService


class FakeDocumentService(AbstractDocumentService):
    async def create(
            self,
            document_in: DocumentIn,
            file_content: bytes = None
    ) -> DocumentOut:
        ...

    async def upload(
            self,
            md5_hash: str,
            file_content: bytes = None
    ):
        ...
