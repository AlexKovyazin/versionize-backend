from documents.src.service.uow import AbstractUnitOfWork


class FakeUnitOfWork(AbstractUnitOfWork):
    """Fake Unit of Work for testing."""

    def __init__(self, session=None):
        self.session = session
        self.committed = False
        self.rolled_back = False
        self.session_closed = False

    async def __aenter__(self):
        return self

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True

    async def close(self):
        self.session_closed = True
