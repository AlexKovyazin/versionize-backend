from documents.src.adapters.repository import AbstractDocumentsRepository, DocumentsRepository
from documents.src.service.uow import AbstractUnitOfWork, UnitOfWork


def get_uow() -> type[AbstractUnitOfWork]:
    """ Function for mock overriding within testing. """
    return UnitOfWork


def get_documents_repository(uow: AbstractUnitOfWork) -> AbstractDocumentsRepository:
    """ Function for mock overriding within testing. """
    return DocumentsRepository(uow)
