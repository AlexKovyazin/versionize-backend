from reviewer.src.adapters.repositories.remark_docs import RemarkDocsRepository
from reviewer.src.domain.remark_doc import RemarkDocIn, RemarkDocOut
from reviewer.src.service.base import GenericService, IRemarkDocService


class RemarkDocService(
    IRemarkDocService,
    GenericService[RemarkDocsRepository, RemarkDocIn, RemarkDocOut]
):
    """ RemarkDocService implementation. """
