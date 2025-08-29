import pytest

from documents.src.service.documents_service import DocumentService
from documents.tests.fixtures.repositories import FakeDocumentsRepository
from documents.tests.fixtures.uow import FakeUnitOfWork


@pytest.fixture
def fake_documents_service():
    """ DocumentService with fake repo and uow. """

    uow = FakeUnitOfWork()
    repo = FakeDocumentsRepository(uow)
    return DocumentService(repo)
