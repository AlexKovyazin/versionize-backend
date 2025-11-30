from uuid import UUID

from fastapi import APIRouter, Depends

from bff.src.adapters.services.identity import CompaniesReadServiceAdapter, CompaniesWriteServiceAdapter
from bff.src.adapters.services.identity import UsersReadServiceAdapter, UsersWriteServiceAdapter
from bff.src.dependencies import get_companies_read_adapter, get_companies_write_adapter
from bff.src.dependencies import get_users_read_adapter, get_users_write_adapter
from bff.src.domain.company import Company, CompaniesSearch, CompaniesUpdate, CompanyBase
from bff.src.domain.user import User, UsersSearch, UserUpdate

router = APIRouter(tags=["Identity"])


@router.get("/users/{user_id}", response_model=User)
async def get_user(
        user_id: UUID,
        adapter: UsersReadServiceAdapter = Depends(get_users_read_adapter)
):
    """Get specified user. """
    return await adapter.get(user_id)


@router.get("/users", response_model=list[User])
async def get_many_users(
        filter_data: UsersSearch = Depends(),
        adapter: UsersReadServiceAdapter = Depends(get_users_read_adapter)
):
    """Get all users by provided fields."""
    return await adapter.list(filter_data)


@router.patch("/users/{user_id}", status_code=202)
async def update_user(
        user_id: UUID,
        data: UserUpdate,
        adapter: UsersWriteServiceAdapter = Depends(get_users_write_adapter)
):
    """ Update specified user. """
    await adapter.update(user_id, data)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
        user_id: UUID,
        adapter: UsersWriteServiceAdapter = Depends(get_users_write_adapter)
):
    """ Delete specified user. """
    await adapter.delete(user_id)


@router.post("/companies", status_code=201)
async def create_company(
        data: CompanyBase,
        adapter: CompaniesWriteServiceAdapter = Depends(get_companies_write_adapter)
):
    """ Create a new company. """
    await adapter.create(data)


@router.get("/companies/{company_id}", response_model=Company)
async def get_company(
        company_id: UUID,
        adapter: CompaniesReadServiceAdapter = Depends(get_companies_read_adapter)
):
    """Get specified company. """
    return await adapter.get(company_id)


@router.get("/companies", response_model=list[Company])
async def get_many_companies(
        filter_data: CompaniesSearch = Depends(),
        adapter: CompaniesReadServiceAdapter = Depends(get_companies_read_adapter)
):
    """Get all companies by provided fields."""
    return await adapter.list(filter_data)


@router.patch("/companies/{company_id}", status_code=202)
async def update_company(
        company_id: UUID,
        data: CompaniesUpdate,
        adapter: CompaniesWriteServiceAdapter = Depends(get_companies_write_adapter)
):
    """ Update specified company. """
    await adapter.update(company_id, data)


@router.delete("/companies/{company_id}", status_code=204)
async def delete_company(
        company_id: UUID,
        adapter: CompaniesWriteServiceAdapter = Depends(get_companies_write_adapter)
):
    """ Delete specified company. """
    await adapter.delete(company_id)
