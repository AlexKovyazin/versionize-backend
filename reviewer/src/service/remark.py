from reviewer.src.service.base import GenericService, IRemarkService
from reviewer.src.domain.remark import RemarkIn, RemarkOut
from reviewer.src.adapters.repositories.remarks import RemarksRepository


class RemarkService(
    IRemarkService,
    GenericService[RemarksRepository, RemarkIn, RemarkOut]
):
    """ RemarkService implementation. """
