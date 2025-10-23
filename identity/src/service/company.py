from identity.src.adapters.repositories.base import ICompaniesRepository
from identity.src.domain.company import Company, CompanyBase
from identity.src.service.base import GenericService, ICompaniesService


class CompaniesService(
    ICompaniesService,
    GenericService[ICompaniesRepository, CompanyBase, Company]
):
    """ CompaniesService implementation. """
