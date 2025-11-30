from pydantic import BaseModel, AnyHttpUrl


class S3DownloadResponse(BaseModel):
    url: AnyHttpUrl
    filename: str
    expires_in: int


class S3UploadResponse(BaseModel):
    url: AnyHttpUrl
    expires_in: int
