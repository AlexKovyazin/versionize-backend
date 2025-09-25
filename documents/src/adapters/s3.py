import abc

import aioboto3
from botocore.exceptions import ClientError

from documents.src.config.settings import settings


class FileExistError(Exception):
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
    async def get(self, file_path: str) -> bytes:
        ...

    @abc.abstractmethod
    async def exists(self, file_path: str) -> bool:
        ...


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

    async def exists(self, file_path, client=None):
        async with client or self.client as s3:
            try:  # if head_object successful - file already exists
                await s3.head_object(Bucket=self.bucket, Key=file_path)
                return True
            except ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    return False
                raise e

    async def put(self, file_path, file_data):
        async with self.client as s3:
            if await self.exists(file_path, client=s3):
                raise FileExistError
            await s3.put_object(Bucket=S3.bucket, Key=file_path, Body=file_data)

    async def delete(self, file_path):
        async with self.client as s3:
            await s3.delete_object(Bucket=S3.bucket, Key=file_path)

    async def get(self, file_path):
        async with self.client as s3:
            document = await s3.get_object(Bucket=S3.bucket, Key=file_path)["Body"].read()
            return document
