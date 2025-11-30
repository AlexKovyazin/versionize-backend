from typing import AsyncIterable

from dishka import provide, Scope, Provider

from documents.src.adapters.repositories.documents import DocumentsRepository
from documents.src.adapters.s3 import S3
from documents.src.service.document import DocumentService
from documents.src.service.uow import UnitOfWork


class DependencyProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_uow(self) -> AsyncIterable[UnitOfWork]:
        """ Real dependency of UnitOfWork for production. """
        async with UnitOfWork() as uow:
            yield uow

    @provide(scope=Scope.REQUEST)
    async def get_s3(self) -> AsyncIterable[S3]:
        """ Real dependency of S3 client for production. """
        async with S3() as s3:
            yield s3

    @provide(scope=Scope.REQUEST)
    async def get_documents_repository(
            self,
            uow: UnitOfWork
    ) -> DocumentsRepository:
        """ Real dependency of DocumentsRepository for production. """
        return DocumentsRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    async def get_documents_service(
            self,
            s3: S3,
            repo: DocumentsRepository,
    ) -> DocumentService:
        """ Real dependency of DocumentService for production. """
        return DocumentService(repo, s3)
