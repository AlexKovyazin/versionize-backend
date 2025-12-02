from projects.src.adapters.orm import OrmDefaultSection
from projects.src.adapters.repositories.base import IDefaultSectionsRepository, GenericRepository
from projects.src.domain.default_section import DefaultSectionIn


class DefaultSectionsRepository(
    IDefaultSectionsRepository,
    GenericRepository[OrmDefaultSection, DefaultSectionIn]
):
    """ DefaultSectionsRepository implementation. """
    ...
