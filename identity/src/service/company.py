from identity.src.adapters.repositories.companies import CompaniesRepository
from identity.src.domain.company import Company, CompanyBase
from identity.src.service.base import GenericService, ICompaniesService


class CompaniesService(
    ICompaniesService,
    GenericService[CompaniesRepository, CompanyBase, Company]
):
    """ CompaniesService implementation. """
