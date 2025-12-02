from projects.src.adapters.repositories.sections import SectionsRepository
from projects.src.domain.section import SectionIn, SectionOut
from projects.src.service.base import GenericService, ISectionService


class SectionService(
    ISectionService,
    GenericService[SectionsRepository, SectionIn, SectionOut]
):
    """ SectionService implementation. """
