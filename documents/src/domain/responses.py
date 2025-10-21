from pydantic import BaseModel, AnyHttpUrl


class DownloadResponse(BaseModel):
    url: AnyHttpUrl
    filename: str
    expires_in: int


class UploadResponse(BaseModel):
    url: AnyHttpUrl
    expires_in: int
