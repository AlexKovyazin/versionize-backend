from typing import AsyncIterable

from dishka import provide, Scope, Provider

from reviewer.src.adapters.repositories.remark_docs import RemarkDocsRepository
from reviewer.src.adapters.repositories.remarks import RemarksRepository
from reviewer.src.service.remark import RemarkService
from reviewer.src.service.remark_doc import RemarkDocService
from reviewer.src.service.uow import UnitOfWork


class DependencyProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_uow(self) -> AsyncIterable[UnitOfWork]:
        """ Real dependency of UnitOfWork for production. """
        async with UnitOfWork() as uow:
            yield uow

    @provide(scope=Scope.REQUEST)
    async def get_remarks_repository(
            self,
            uow: UnitOfWork
    ) -> RemarksRepository:
        """ Real dependency of RemarksRepository for production. """
        return RemarksRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    async def get_remark_service(
            self,
            repo: RemarksRepository,
    ) -> RemarkService:
        """ Real dependency of RemarkService for production. """
        return RemarkService(repo)

    @provide(scope=Scope.REQUEST)
    async def get_remark_docs_repository(
            self,
            uow: UnitOfWork
    ) -> RemarkDocsRepository:
        """ Real dependency of RemarkDocsRepository for production. """
        return RemarkDocsRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    async def get_remark_doc_service(
            self,
            repo: RemarkDocsRepository,
    ) -> RemarkDocService:
        """ Real dependency of RemarkDocService for production. """
        return RemarkDocService(repo)
