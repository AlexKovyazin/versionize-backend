from reviewer.src.adapters.orm import OrmRemarkDoc
from reviewer.src.adapters.repositories.base import IRemarkDocsRepository, GenericRepository
from reviewer.src.domain.remark_doc import RemarkDocIn


class RemarkDocsRepository(
    IRemarkDocsRepository,
    GenericRepository[OrmRemarkDoc, RemarkDocIn]
):
    """ RemarkDocsRepository implementation. """
    ...
