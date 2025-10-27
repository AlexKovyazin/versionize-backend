from projects.src.adapters.orm import OrmSection, OrmDefaultSection
from projects.src.adapters.repositories.base import GenericRepository, ISectionsRepository, IDefaultSectionsRepository
from projects.src.domain.section import SectionIn, DefaultSectionIn


class DefaultSectionsRepository(
    IDefaultSectionsRepository,
    GenericRepository[OrmDefaultSection, DefaultSectionIn]
):
    """ DefaultSectionsRepository implementation. """
    ...


class SectionsRepository(
    ISectionsRepository,
    GenericRepository[OrmSection, SectionIn]
):
    """ SectionsRepository implementation. """
    ...
