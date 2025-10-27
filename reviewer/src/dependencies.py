import httpx
from fastapi import Depends, HTTPException

from reviewer.src.config.settings import settings
from reviewer.src.domain.user import User
from reviewer.src.service.auth import oauth2_scheme
from reviewer.src.service.uow import UnitOfWork
from reviewer.src.adapters.repositories.remarks import RemarksRepository
from reviewer.src.adapters.repositories.remark_docs import RemarkDocsRepository
from reviewer.src.service.remark import RemarkService
from reviewer.src.service.remark_doc import RemarkDocService


async def get_user(token: str = Depends(oauth2_scheme)):
    """ Real dependency for authenticating of user by identity service. """

    # TODO maybe it should be refactor for using IdentityService class,
    #  not straight call with request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.auth_service_url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise

    return User.model_validate(response.json())


async def get_uow():
    """ Real dependency of UnitOfWork for production. """
    async with UnitOfWork() as uow:
        yield uow


async def get_remarks_repository(
        uow=Depends(get_uow)
) -> RemarksRepository:
    """ Real dependency of RemarksRepository for production. """
    return RemarksRepository(uow=uow)


async def get_remark_docs_repository(
        uow=Depends(get_uow)
) -> RemarkDocsRepository:
    """ Real dependency of RemarkDocsRepository for production. """
    return RemarkDocsRepository(uow=uow)


async def get_remark_service(
        repo=Depends(get_remarks_repository),
) -> RemarkService:
    """ Real dependency of RemarkService for production. """
    return RemarkService(repo)


async def get_remark_doc_service(
        repo=Depends(get_remark_docs_repository),
) -> RemarkDocService:
    """ Real dependency of RemarkDocService for production. """
    return RemarkDocService(repo)
