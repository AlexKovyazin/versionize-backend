from reviewer.src.adapters.orm import OrmRemark
from reviewer.src.adapters.repositories.base import IRemarksRepository, GenericRepository
from reviewer.src.domain.remark import RemarkIn


class RemarksRepository(
    IRemarksRepository,
    GenericRepository[OrmRemark, RemarkIn]
):
    """ RemarksRepository implementation. """
    ...
