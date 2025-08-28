from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from documents.src.config import get_db_url
from documents.src.settings import settings

async_engine = create_async_engine(
    get_db_url(sync=False),
    future=True,
)

ASYNC_SESSION_FACTORY = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class UnitOfWork:
    def __init__(self, session_factory=ASYNC_SESSION_FACTORY):
        # session_factory could be a mocked object that don't touch db
        self.session_factory = session_factory
        self.session = None

    async def __aenter__(self):
        if not self.session:
            self.session = self.session_factory()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        # Session wasn't initialized, possibly due to an error in __aenter__
        if self.session is None:
            return

        # TODO: need to add logging to exception catching
        try:
            if exc_type is None:
                await self.session.commit()
            else:
                await self.session.rollback()
        except Exception as e:
            await self.session.rollback()
        finally:
            await self.session.close()
            self.session = None


def get_uow() -> type[UnitOfWork]:
    if settings.is_test:
        # TODO: return mocked uow
        pass
    return UnitOfWork
