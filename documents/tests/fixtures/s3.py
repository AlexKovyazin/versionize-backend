from typing import AsyncGenerator
from uuid import UUID

from documents.src.adapters.s3 import AbstractS3, FileExistError
from documents.src.enums import DocumentContentType


class FakeS3(AbstractS3):
    """In-memory fake S3 for testing."""

    def __init__(self, documents: dict | None = None):
        self.documents = documents or {}
        super().__init__()

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc, tb):
        ...

    async def put(self, file_path: str, file_data: bytes) -> None:
        if await self.exists(file_path):
            raise FileExistError
        self.documents[file_path] = file_data

    async def delete(self, file_path: str) -> None:
        self.documents.pop(file_path, None)

    async def get(self, file_path: str) -> bytes:
        return self.documents[file_path]

    async def exists(self, file_path: str) -> bool:
        return True if self.documents.get(file_path) else False

    async def get_stream(
            self,
            file_path: str,
            chunk_size: int = 1024
    ) -> AsyncGenerator:
        ...

    async def get_download_url(self, file_path: str | UUID) -> str:
        return "https://testing-link.com"

    async def get_upload_url(
            self,
            file_path: str | UUID,
            file_type: str = DocumentContentType.PDF.value
    ) -> str:
        return "https://testing-link.com"
