from identity.src.adapters.orm import OrmUser
from identity.src.adapters.repositories.base import GenericRepository, AbstractUsersRepository
from identity.src.config.logging import logger
from identity.src.domain.user import UserBase


class UsersRepository(
    AbstractUsersRepository,
    GenericRepository[OrmUser, UserBase]
):
    async def create(self, user: UserBase) -> OrmUser:
        logger.info(
            f"Adding new OrmUser with id {user.id}...",
            extra=user.model_dump()
        )

        # difference here
        db_user = OrmUser(**user.model_dump(exclude={"roles"}))

        self.uow.session.add(db_user)
        await self.uow.session.flush()

        logger.info(
            f"New user {user.id} added to DB",
            extra=db_user.to_dict()
        )
        return db_user
