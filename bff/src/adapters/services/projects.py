from bff.src.adapters.broker.cmd import ProjectCmd, DefaultSectionCmd
from bff.src.adapters.services.base import GenericServiceReadAdapter, IProjectsWriteServiceAdapter
from bff.src.adapters.services.base import GenericServiceWriteAdapter
from bff.src.adapters.services.base import IDefaultSectionsReadServiceAdapter
from bff.src.adapters.services.base import IDefaultSectionsWriteServiceAdapter
from bff.src.adapters.services.base import IProjectsReadServiceAdapter
from bff.src.domain.project import ProjectIn, ProjectUpdate
from bff.src.domain.project import ProjectsSearchParams, ProjectOut
from bff.src.domain.section import DefaultSectionIn, DefaultSectionUpdate
from bff.src.domain.section import DefaultSectionsSearch, DefaultSectionOut


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


class DefaultSectionsReadServiceAdapter(
    IDefaultSectionsReadServiceAdapter,
    GenericServiceReadAdapter[DefaultSectionsSearch, DefaultSectionOut]
):
    ...


class DefaultSectionsWriteServiceAdapter(
    IDefaultSectionsWriteServiceAdapter,
    GenericServiceWriteAdapter[DefaultSectionCmd, DefaultSectionIn, DefaultSectionUpdate]
):
    ...
