from fastapi import Depends

from documents.src.adapters.repository import AbstractDocumentsRepository, DocumentsRepository
from documents.src.service.documents_service import DocumentService
from documents.src.service.uow import UnitOfWork


async def get_uow():
    """ Real dependency of UnitOfWork for production. """
    uow = UnitOfWork()
    async with uow:
        yield uow


def get_documents_repository(uow=Depends(get_uow)) -> AbstractDocumentsRepository:
    """ Real dependency of DocumentsService for production. """
    return DocumentsRepository(uow)


def get_document_service(repo=Depends(get_documents_repository)):
    """ Real dependency of DocumentsService for production. """
    return DocumentService(repo)
