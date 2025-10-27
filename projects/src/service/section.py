from projects.src.adapters.repositories.sections import SectionsRepository, DefaultSectionsRepository
from projects.src.domain.section import DefaultSectionIn, DefaultSectionOut
from projects.src.domain.section import SectionIn, SectionOut
from projects.src.service.base import GenericService, ISectionService, IDefaultSectionService


class DefaultSectionService(
    IDefaultSectionService,
    GenericService[DefaultSectionsRepository, DefaultSectionIn, DefaultSectionOut]
):
    """ DefaultSectionService implementation. """


class SectionService(
    ISectionService,
    GenericService[SectionsRepository, SectionIn, SectionOut]
):
    """ SectionService implementation. """
