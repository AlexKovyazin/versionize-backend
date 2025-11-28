from bff.src.adapters.broker.cmd import ProjectCmd, DefaultSectionCmd, SectionCmd
from bff.src.adapters.services.base import GenericServiceReadAdapter, GenericServiceWriteAdapter
from bff.src.adapters.services.base import IDefaultSectionsReadServiceAdapter, IDefaultSectionsWriteServiceAdapter
from bff.src.adapters.services.base import IProjectsReadServiceAdapter, IProjectsWriteServiceAdapter
from bff.src.adapters.services.base import ISectionsReadServiceAdapter, ISectionsWriteServiceAdapter
from bff.src.domain.project import ProjectIn, ProjectUpdate
from bff.src.domain.project import ProjectsSearchParams, ProjectOut
from bff.src.domain.section import DefaultSectionIn, DefaultSectionUpdate
from bff.src.domain.section import DefaultSectionsSearch, DefaultSectionOut
from bff.src.domain.section import SectionIn, SectionUpdate
from bff.src.domain.section import SectionsSearch, SectionOut


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


class SectionsReadServiceAdapter(
    ISectionsReadServiceAdapter,
    GenericServiceReadAdapter[SectionsSearch, SectionOut]
):
    ...


class SectionsWriteServiceAdapter(
    ISectionsWriteServiceAdapter,
    GenericServiceWriteAdapter[SectionCmd, SectionIn, SectionUpdate]
):
    ...
