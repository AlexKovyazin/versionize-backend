from bff.src.adapters.broker.cmd import CompanyCmd
from bff.src.adapters.broker.cmd import UserCmd
from bff.src.adapters.services.base import GenericServiceReadAdapter, GenericServiceWriteAdapter
from bff.src.adapters.services.base import ICompaniesReadServiceAdapter, ICompaniesWriteServiceAdapter
from bff.src.adapters.services.base import IUsersReadServiceAdapter, IUsersWriteServiceAdapter
from bff.src.domain.company import Company, CompanyBase, CompaniesSearch, CompaniesUpdate
from bff.src.domain.user import User, UsersSearch, UserUpdate


class UsersReadServiceAdapter(
    IUsersReadServiceAdapter,
    GenericServiceReadAdapter[UsersSearch, User]
):
    ...


class UsersWriteServiceAdapter(
    IUsersWriteServiceAdapter,
    GenericServiceWriteAdapter[UserCmd, User, UserUpdate]
):
    async def create(self, entity, **kwargs):
        raise NotImplementedError("Create operation is not supported for UserService")


class CompaniesReadServiceAdapter(
    ICompaniesReadServiceAdapter,
    GenericServiceReadAdapter[CompaniesSearch, Company]
):
    ...


class CompaniesWriteServiceAdapter(
    ICompaniesWriteServiceAdapter,
    GenericServiceWriteAdapter[CompanyCmd, CompanyBase, CompaniesUpdate]
):
    ...
