import abc
from uuid import UUID

from identity.src.adapters.repository import AbstractUsersRepository
from identity.src.domain.user import User


class AbstractUserService(abc.ABC):
    def __init__(
            self,
            repository: AbstractUsersRepository,
    ):
        self.repository = repository

    @abc.abstractmethod
    async def get(self, **kwargs) -> User:
        ...

    @abc.abstractmethod
    async def get_many(self, **kwargs) -> list[User]:
        ...

    @abc.abstractmethod
    async def update(self, user_id: UUID, **kwargs) -> User:
        ...

    @abc.abstractmethod
    async def delete(self, user_id: UUID) -> None:
        ...


class UserService(AbstractUserService):
    async def get(self, **kwargs) -> User:
        db_user = await self.repository.get(**kwargs)
        return User.model_validate(db_user)

    async def get_many(self, **kwargs) -> list[User]:
        db_users = await self.repository.get_many(**kwargs)
        return [User.model_validate(d) for d in db_users]

    async def update(self, user_id: UUID, **kwargs) -> User:
        updated_user = await self.repository.update(user_id, **kwargs)
        updated_user = User.model_validate(updated_user)
        return updated_user

    async def delete(self, user_id: UUID) -> None:
        await self.repository.delete(user_id)
