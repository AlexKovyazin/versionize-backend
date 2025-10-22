from uuid import UUID

import httpx
from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from documents.src.adapters.repositories.base import AbstractDocumentsRepository
from documents.src.adapters.repositories.documents import DocumentsRepository
from documents.src.adapters.s3 import S3
from documents.src.config.settings import settings
from documents.src.domain.document import DocumentsSearch
from documents.src.domain.user import User
from documents.src.service.auth import oauth2_scheme
from documents.src.service.documents_service import DocumentService
from documents.src.service.uow import UnitOfWork


async def get_uow():
    """ Real dependency of UnitOfWork for production. """
    async with UnitOfWork() as uow:
        yield uow


async def get_s3():
    """ Real dependency of S3 client for production. """
    async with S3() as s3:
        yield s3


def get_documents_repository(uow=Depends(get_uow)) -> AbstractDocumentsRepository:
    """ Real dependency of DocumentsService for production. """
    return DocumentsRepository(uow)


def get_document_service(
        repo=Depends(get_documents_repository),
        s3=Depends(get_s3),
):
    """ Real dependency of DocumentsService for production. """
    return DocumentService(repo, s3)


async def get_user(token: str = Depends(oauth2_scheme)):
    """ Real dependency for authenticating of user by identity service. """

    # TODO maybe it should be refactor for using IdentityService class,
    #  not straight call with request
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.auth_service_url,
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()

    return User.model_validate(response.json())


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
