from identity.src.adapters.orm import OrmCompany
from identity.src.adapters.repositories.base import GenericRepository, ICompaniesRepository
from identity.src.domain.company import CompanyBase


class CompaniesRepository(
    ICompaniesRepository,
    GenericRepository[OrmCompany, CompanyBase]
):
    """ CompaniesRepository implementation. """
