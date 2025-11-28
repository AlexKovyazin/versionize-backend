from bff.src.adapters.broker.cmd import ProjectCmd
from bff.src.adapters.services.base import GenericServiceReadAdapter, IProjectsWriteServiceAdapter
from bff.src.adapters.services.base import GenericServiceWriteAdapter
from bff.src.adapters.services.base import IProjectsReadServiceAdapter
from bff.src.domain.project import ProjectIn
from bff.src.domain.project import ProjectUpdate
from bff.src.domain.project import ProjectsSearchParams, ProjectOut


class ProjectsReadServiceAdapter(
    IProjectsReadServiceAdapter,
    GenericServiceReadAdapter[ProjectsSearchParams, ProjectOut]
):
    ...


class ProjectsWriteServiceAdapter(
    IProjectsWriteServiceAdapter,
    GenericServiceWriteAdapter[ProjectCmd, ProjectIn, ProjectUpdate]
):
    ...
