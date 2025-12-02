from projects.src.adapters.repositories.default_sections import DefaultSectionsRepository
from projects.src.domain.default_section import DefaultSectionIn, DefaultSectionOut
from projects.src.service.base import GenericService, IDefaultSectionService


class DefaultSectionService(
    IDefaultSectionService,
    GenericService[DefaultSectionsRepository, DefaultSectionIn, DefaultSectionOut]
):
    """ DefaultSectionService implementation. """
