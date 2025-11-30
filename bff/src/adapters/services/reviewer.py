from bff.src.adapters.broker.cmd import RemarkCmd, RemarkDocCmd
from bff.src.adapters.services.base import GenericServiceReadAdapter, GenericServiceWriteAdapter
from bff.src.adapters.services.base import IRemarkDocsReadServiceAdapter, IRemarkDocsWriteServiceAdapter
from bff.src.adapters.services.base import IRemarksReadServiceAdapter, IRemarksWriteServiceAdapter
from bff.src.domain.remark import RemarksSearch, RemarkOut, RemarkUpdate, RemarkIn
from bff.src.domain.remark_doc import RemarkDocsSearch, RemarkDocOut, RemarkDocUpdate, RemarkDocIn


class RemarksReadServiceAdapter(
    IRemarksReadServiceAdapter,
    GenericServiceReadAdapter[RemarksSearch, RemarkOut]
):
    ...


class RemarksWriteServiceAdapter(
    IRemarksWriteServiceAdapter,
    GenericServiceWriteAdapter[RemarkCmd, RemarkIn, RemarkUpdate]
):
    ...


class RemarkDocsReadServiceAdapter(
    IRemarkDocsReadServiceAdapter,
    GenericServiceReadAdapter[RemarkDocsSearch, RemarkDocOut]
):
    ...


class RemarkDocsWriteServiceAdapter(
    IRemarkDocsWriteServiceAdapter,
    GenericServiceWriteAdapter[RemarkDocCmd, RemarkDocIn, RemarkDocUpdate]
):
    ...
