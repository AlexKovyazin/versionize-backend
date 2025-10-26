from fastapi import Depends

from documents.src.adapters.repositories.base import IDocumentsRepository
from documents.src.dependencies import get_uow
from documents.tests.fixtures.repositories import FakeDocumentsRepository
from documents.tests.fixtures.uow import FakeUnitOfWork


async def fake_uow():
    """ Fake dependency of UnitOfWork for tests. """
    uow = FakeUnitOfWork()
    async with uow:
        yield uow


def fake_documents_repository(uow=Depends(get_uow)) -> IDocumentsRepository:
    """ Fake dependency of documents repo for tests. """
    return FakeDocumentsRepository(uow)
