import datetime
import hashlib
import uuid

import pytest

from documents.src.adapters.orm import OrmDocument
from documents.src.domain.document import DocumentOut
from documents.src.service.documents_service import DocumentService
from documents.tests.fixtures.factories import create_document_in_data
from documents.tests.fixtures.repositories import FakeDocumentsRepository
from documents.tests.fixtures.uow import FakeUnitOfWork
from documents.tests.fixtures.s3 import FakeS3


@pytest.fixture
def fake_documents_service() -> DocumentService:
    """ DocumentService with fake repo and uow. """

    uow = FakeUnitOfWork()
    repo = FakeDocumentsRepository(uow)
    s3 = FakeS3()
    return DocumentService(repo, s3)


@pytest.fixture
def default_first_document() -> DocumentOut:
    """ Default first version of a document. """

    document_in_data = create_document_in_data()
    document_orm = OrmDocument(
        id=uuid.uuid4(),
        version=1,
        variation=0,
        md5=hashlib.md5().hexdigest(),
        created_at=datetime.datetime.now(),
        **document_in_data.model_dump(),
    )
    return DocumentOut.model_validate(document_orm)


@pytest.fixture
def make_two_versions_of_a_document() -> callable:
    def _factory(raise_variation=False) -> list[DocumentOut]:
        document_in_data = create_document_in_data(
            name="Document of a specific section",
            note="First variation"
        )
        first_document_orm = OrmDocument(
            id=uuid.uuid4(),
            version=1,
            variation=0,
            md5=hashlib.md5().hexdigest(),
            created_at=datetime.datetime.now(),
            **document_in_data,
        )

        document_in_data["note"] = "Second variation"
        second_document_variation = 1 if raise_variation else 0
        second_document_version = first_document_orm.version + 1
        second_document_orm = OrmDocument(
            id=uuid.uuid4(),
            version=second_document_version,
            variation=second_document_variation,
            md5=hashlib.md5().hexdigest(),
            created_at=datetime.datetime.now(),
            **document_in_data,
        )
        return [
            DocumentOut.model_validate(first_document_orm),
            DocumentOut.model_validate(second_document_orm)
        ]

    return _factory
