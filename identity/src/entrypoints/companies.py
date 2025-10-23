from uuid import UUID

from fastapi import APIRouter, Depends

from identity.src.dependencies import get_companies_service, get_companies_search_params
from identity.src.domain.company import Company, CompanyBase, CompaniesSearch, CompaniesUpdate
from identity.src.service.company import CompaniesService

router = APIRouter(tags=["Companies"])


@router.post("", response_model=Company, status_code=201)
async def create(
        data: CompanyBase,
        companies_service: CompaniesService = Depends(get_companies_service),
):
    """ Create a new company. """
    return await companies_service.create(data)


@router.get("/{company_id}", response_model=Company)
async def get(
        company_id: UUID,
        companies_service: CompaniesService = Depends(get_companies_service),
):
    """Get specified company. """
    return await companies_service.get(id=company_id)


@router.get("", response_model=list[Company])
async def get_many(
        data: CompaniesSearch = Depends(get_companies_search_params),
        companies_service: CompaniesService = Depends(get_companies_service),
):
    """Get all companies by provided fields."""
    return await companies_service.get_many(
        **data.model_dump(exclude_none=True)
    )


@router.patch("/{company_id}", response_model=Company, status_code=202)
async def update(
        company_id: UUID,
        data: CompaniesUpdate,
        companies_service: CompaniesService = Depends(get_companies_service)
):
    """ Update specified companies. """
    document = await companies_service.update(
        company_id,
        **data.model_dump(exclude_none=True)
    )
    return document


@router.delete("/{company_id}", status_code=204)
async def delete(
        company_id: UUID,
        companies_service: CompaniesService = Depends(get_companies_service),
):
    """ Delete specified companies. """
    await companies_service.delete(company_id)
