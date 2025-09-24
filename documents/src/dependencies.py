from fastapi import Depends

from documents.src.adapters.repository import AbstractDocumentsRepository, DocumentsRepository
from documents.src.service.documents_service import DocumentService
from documents.src.service.uow import UnitOfWork
from documents.src.adapters.s3 import AbstractS3, S3


async def get_uow():
    """ Real dependency of UnitOfWork for production. """
    uow = UnitOfWork()
    async with uow:
        yield uow


def get_documents_repository(uow=Depends(get_uow)) -> AbstractDocumentsRepository:
    """ Real dependency of DocumentsService for production. """
    return DocumentsRepository(uow)


def get_s3() -> AbstractS3:
    """ Real dependency of S3 for production. """
    return S3()


def get_document_service(
        repo=Depends(get_documents_repository),
        s3=Depends(get_s3),
):
    """ Real dependency of DocumentsService for production. """
    return DocumentService(repo, s3)
