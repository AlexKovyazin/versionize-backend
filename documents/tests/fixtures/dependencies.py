from fastapi import Depends

from src.adapters.repositories.base import IDocumentsRepository
from src.dependencies import get_uow
from tests.fixtures.repositories import FakeDocumentsRepository
from tests.fixtures.uow import FakeUnitOfWork


async def fake_uow():
    """ Fake dependency of UnitOfWork for tests. """
    uow = FakeUnitOfWork()
    async with uow:
        yield uow


def fake_documents_repository(uow=Depends(get_uow)) -> IDocumentsRepository:
    """ Fake dependency of documents repo for tests. """
    return FakeDocumentsRepository(uow)
