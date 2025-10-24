from identity.src.adapters.repositories.users import UsersRepository
from identity.src.domain.user import User, UserBase
from identity.src.service.base import IUserService, GenericService


class UserService(
    IUserService,
    GenericService[UsersRepository, UserBase, User]
):
    """ UserService implementation. """

    async def create(self, entity: UserBase, **kwargs):
        raise NotImplementedError("Create operation is not supported for UserService")
