import abc
from typing import AsyncGenerator

import aioboto3
from botocore.exceptions import ClientError

from documents.src.config.logging import logger
from documents.src.config.settings import settings


class FileExistError(Exception):
    ...


class FileNotExistError(Exception):
    ...


class AbstractS3(abc.ABC):
    endpoint: str
    bucket: str

    @abc.abstractmethod
    async def put(self, file_path: str, file_data: bytes) -> None:
        ...

    @abc.abstractmethod
    async def delete(self, file_path: str) -> None:
        ...

    @abc.abstractmethod
    async def get(self, file_path: str, chunk_size: int = 1024) -> AsyncGenerator:
        ...

    @abc.abstractmethod
    async def exists(self, file_path: str) -> bool:
        ...


class S3Stream:
    """ Class for getting AsyncGenerator streams of S3 files. """

    def __init__(self, client, file_path: str, chunk_size: int = 1024 * 128):
        self.client = client
        self.file_path = file_path
        self.chunk_size = chunk_size

    async def __aiter__(self):
        async with self.client as s3:
            try:
                document = await s3.get_object(
                    Bucket=S3.bucket,
                    Key=self.file_path
                )
                stream = document["Body"]
                while file_data := await stream.read(self.chunk_size):
                    yield file_data
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'NoSuchKey':
                    raise FileNotExistError(
                        f"File {self.file_path} not found in S3"
                    )
                raise e


class S3(AbstractS3):
    endpoint: str = settings.s3_endpoint.get_secret_value()
    bucket: str = settings.s3_bucket.get_secret_value()

    def __init__(self):
        self.client = aioboto3.Session().client(
            service_name="s3",
            region_name=settings.s3_region.get_secret_value(),
            aws_access_key_id=settings.s3_access_key.get_secret_value(),
            aws_secret_access_key=settings.s3_secret_key.get_secret_value(),
            endpoint_url=S3.endpoint
        )

    async def exists(self, file_path, client=None) -> bool:
        async with client or self.client as s3:
            try:  # if head_object successful - file already exists
                await s3.head_object(Bucket=self.bucket, Key=file_path)
                return True
            except ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    return False
                raise e

    async def put(
            self,
            file_path: str,
            file_data: bytes
    ) -> None:
        logger.info(f"Putting document {file_path} to S3...")

        async with self.client as s3:
            if await self.exists(file_path, client=s3):
                raise FileExistError
            await s3.put_object(Bucket=S3.bucket, Key=file_path, Body=file_data)

        logger.info(f"Document {file_path} successfully added to S3")

    async def delete(self, file_path: str) -> None:
        logger.info(f"Deleting document {file_path} from S3...")

        async with self.client as s3:
            await s3.delete_object(Bucket=S3.bucket, Key=file_path)

        logger.info(f"Document {file_path} successfully deleted from S3")

    async def get(
            self,
            file_path: str,
            chunk_size: int = 1024 * 128,
    ) -> S3Stream:
        """  Getting stream of file from S3. """

        async with self.client as s3:
            return S3Stream(s3, file_path, chunk_size=chunk_size)
