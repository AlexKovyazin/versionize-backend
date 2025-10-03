from uuid import UUID

from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from documents.src.adapters.repository import AbstractDocumentsRepository, DocumentsRepository
from documents.src.adapters.s3 import AbstractS3, S3
from documents.src.domain.schemas.document import DocumentsSearch
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


def get_s3() -> AbstractS3:
    """ Real dependency of S3 for production. """
    return S3()


def get_document_service(
        repo=Depends(get_documents_repository),
        s3=Depends(get_s3),
):
    """ Real dependency of DocumentsService for production. """
    return DocumentService(repo, s3)


async def get_search_params(
        document_id: UUID | None = None,
        company_id: UUID | None = None,
        project_id: UUID | None = None,
        section_id: UUID | None = None,
        responsible_id: UUID | None = None,
) -> DocumentsSearch:
    """ Dependency for parsing query results of get requests for getting documents. """

    try:
        search_data = DocumentsSearch(
            id=document_id,
            company_id=company_id,
            project_id=project_id,
            section_id=section_id,
            responsible_id=responsible_id
        )
    except ValidationError as e:
        raise RequestValidationError(e.errors())

    return search_data
