from projects.src.adapters.orm import OrmSection
from projects.src.adapters.repositories.base import GenericRepository, ISectionsRepository
from projects.src.domain.section import SectionIn


class SectionsRepository(
    ISectionsRepository,
    GenericRepository[OrmSection, SectionIn]
):
    """ SectionsRepository implementation. """
    ...
