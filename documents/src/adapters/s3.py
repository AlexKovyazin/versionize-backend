import abc
from typing import AsyncGenerator

import aioboto3
import aiobotocore.client
from aiobotocore.session import ClientCreatorContext
from botocore.exceptions import ClientError

from documents.src.config.logging import logger
from documents.src.config.settings import settings


def get_s3_session_context():
    return aioboto3.Session().client(
        service_name="s3",
        region_name=settings.s3_region.get_secret_value(),
        aws_access_key_id=settings.s3_access_key.get_secret_value(),
        aws_secret_access_key=settings.s3_secret_key.get_secret_value(),
        endpoint_url=settings.s3_endpoint.get_secret_value()
    )


class FileExistError(Exception):
    ...


class FileNotExistError(Exception):
    ...


class AbstractS3(abc.ABC):
    endpoint: str = settings.s3_endpoint.get_secret_value()
    bucket: str = settings.s3_bucket.get_secret_value()
    _client: aiobotocore.client.AioBaseClient | None
    _context: ClientCreatorContext | None

    def __init__(self):
        self._client = None
        self._context = None

    @abc.abstractmethod
    async def __aenter__(self):
        ...

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        ...

    @abc.abstractmethod
    async def put(self, file_path: str, file_data: bytes) -> None:
        ...

    @abc.abstractmethod
    async def get_stream(self, file_path: str, chunk_size: int = 1024) -> AsyncGenerator:
        ...

    @abc.abstractmethod
    async def exists(self, file_path: str) -> bool:
        ...

    @abc.abstractmethod
    async def delete(self, file_path: str) -> None:
        ...


class S3Stream:
    """
    Class for getting AsyncGenerator streams of S3 files.

    S3Stream has its own s3 connection due to aioboto3's specific issues
    with closing the streaming connection.
    """

    def __init__(
            self,
            file_path: str,
            chunk_size: int = 1024 * 128
    ):
        self.file_path = file_path
        self.chunk_size = chunk_size

    async def __aiter__(self):
        async with get_s3_session_context() as client:
            try:
                response = await client.get_object(
                    Bucket=S3.bucket,
                    Key=self.file_path
                )
                stream = response["Body"]
                async with stream:
                    while file_data := await stream.read(self.chunk_size):
                        yield file_data

            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "NoSuchKey":
                    raise FileNotExistError(
                        f"File {self.file_path} not found in S3"
                    )
                raise e


class S3(AbstractS3):
    """
    S3 adapter class.

    Use dependency injection or async context manager to use it.

    Examples:
        def get_document_service(
                repo=Depends(get_documents_repository),
                s3=Depends(get_s3_client),
        ):
            ...

        async with S3() as s3:
            s3.exists("document_path_as_string")
            s3.get("document_path_as_string")

    Note:
        If you use S3 through dependency injection
        the resulting instance of the class will use single connection until dependency close it.
    """

    endpoint: str = settings.s3_endpoint.get_secret_value()
    bucket: str = settings.s3_bucket.get_secret_value()
    _client: aiobotocore.client.AioBaseClient | None
    _context: ClientCreatorContext | None

    async def __aenter__(self):
        self._context = get_s3_session_context()
        self._client = await self._context.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._context and self._client:
            await self._context.__aexit__(exc_type, exc, tb)
            self._client = None
            self._context = None

    async def put(
            self,
            file_path: str,
            file_data: bytes
    ) -> None:
        """ Upload file to specified path. """

        logger.info(f"Putting document {file_path} to S3...")

        if await self.exists(file_path):
            raise FileExistError
        await self._client.put_object(Bucket=S3.bucket, Key=file_path, Body=file_data)

        logger.info(f"Document {file_path} successfully added to S3")

    async def get_stream(
            self,
            file_path: str,
            chunk_size: int = 1024 * 128,
    ) -> S3Stream:
        """  Getting stream of file from S3. """

        return S3Stream(file_path, chunk_size=chunk_size)

    async def exists(self, file_path) -> bool:
        """ Check if file exists without getting file itself. """

        try:  # if head_object successful - file already exists
            await self._client.head_object(Bucket=self.bucket, Key=file_path)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise e

    async def delete(self, file_path: str) -> None:
        """  Delete specified file. """

        logger.info(f"Deleting document {file_path} from S3...")
        await self._client.delete_object(Bucket=S3.bucket, Key=file_path)
        logger.info(f"Document {file_path} successfully deleted from S3")
