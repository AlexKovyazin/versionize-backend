import abc
from typing import Sequence

from sqlalchemy import Select, select
from sqlalchemy.orm import InstrumentedAttribute, load_only, defer

from identity.src.adapters.orm import OrmUser
from identity.src.config.logging import logger
from identity.src.domain.user import UserBase
from identity.src.service.uow import AbstractUnitOfWork


class AbstractUsersRepository(abc.ABC):
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    @abc.abstractmethod
    async def create(self, user: UserBase) -> OrmUser:
        ...

    @abc.abstractmethod
    async def get(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> OrmUser:
        ...



class UsersRepository(AbstractUsersRepository):

    async def create(self, user: UserBase) -> OrmUser:
        logger.info(
            f"Adding new user {user.id}...",
            extra=user.model_dump()
        )
        db_user = OrmUser(**user.model_dump(exclude={"roles"}))
        self.uow.session.add(db_user)
        await self.uow.session.flush()

        logger.info(
            f"New user {user.id} added to DB",
            extra=db_user.to_dict()
        )
        return db_user

    async def get(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> OrmUser:
        """
        Get specified user from DB.

        @:param include_fields: Sequence of OrmUser fields to include into output object.
        @:param exclude_fields: Sequence of OrmUser fields to exclude from output object.
        @:param kwargs: Filter keywords.

        Example with documents:
        self.get(
          name="Specific document name",
          include_fields=(OrmDocument.section_id, OrmDocument.md5,)
        )
        This call will filter documents by specified name and query only fields of include_fields argument.

        SQL query will be:
        SELECT section_id, md5
          FROM documents
         WHERE name = 'Specific document name'
         ORDER BY created_at DESC
         LIMIT 1
        """

        query = await self._prepare_select(
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            **kwargs
        )
        query_result = await self.uow.session.execute(query)
        document = query_result.scalar_one_or_none()

        return document

    async def _prepare_select(
            self,
            include_fields: Sequence[InstrumentedAttribute] = (),
            exclude_fields: Sequence[InstrumentedAttribute] = (),
            **kwargs
    ) -> Select:
        """
        Prepare select query.

        Filter objects by specified kwargs,
        Filter fields to include in output query,
        order results by descending created_at field.
        """

        query = (
            select(OrmUser)
            .filter_by(**kwargs)
            .order_by(OrmUser.created_at.desc())
        )
        if include_fields:
            query = query.options(load_only(*include_fields))
        if exclude_fields:
            query = query.options(defer(*exclude_fields))

        return query