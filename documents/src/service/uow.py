import abc

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from documents.src.settings import settings


async_engine = create_async_engine(
    settings.async_db_url,
    future=True,
)

ASYNC_SESSION_FACTORY = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class AbstractUnitOfWork(abc.ABC):
    @abc.abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_value, traceback):
        # TODO: need to add logging to exception catching
        try:
            if exc_type is None:
                await self.commit()
        finally:
            await self.rollback()
            await self.close()
            self.session = None

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=ASYNC_SESSION_FACTORY):
        # session_factory could be a mocked object that don't touch db
        self.session_factory = session_factory
        self.session = None

    async def __aenter__(self):
        if not self.session:
            self.session = self.session_factory()
        return self

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()
