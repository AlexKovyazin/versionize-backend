from fastapi import Depends

from documents.src.adapters.repositories.base import IDocumentsRepository
from documents.src.dependencies import get_uow, get_documents_repository
from documents.tests.fixtures.repositories import FakeDocumentsRepository
from documents.tests.fixtures.services import FakeDocumentService
from documents.tests.fixtures.uow import FakeUnitOfWork


async def fake_uow():
    """ Fake dependency of UnitOfWork for tests. """
    uow = FakeUnitOfWork()
    async with uow:
        yield uow


def fake_documents_repository(uow=Depends(get_uow)) -> IDocumentsRepository:
    """ Fake dependency of documents repo for tests. """
    return FakeDocumentsRepository(uow)


def fake_document_service(repo=Depends(get_documents_repository)):
    """ Fake dependency of documents service for tests. """
    return FakeDocumentService(repo)
