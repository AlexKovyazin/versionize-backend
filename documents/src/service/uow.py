from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from documents.src.settings import settings

connect_args = {"check_same_thread": False}
DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        settings.DB_URL.get_secret_value(),
        connect_args=connect_args,
    )
)


class UnitOfWork:
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
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
        except Exception as e:
            a = 1
        finally:
            await self.session.rollback()
            await self.session.close()
            self.session = None


def get_uow() -> type[UnitOfWork]:
    if settings.IS_TEST:
        # TODO: return mocked uow
        pass
    return UnitOfWork
