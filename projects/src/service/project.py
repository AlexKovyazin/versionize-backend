from projects.src.service.base import GenericService, IProjectService
from projects.src.domain.project import ProjectIn, ProjectOut
from projects.src.adapters.repositories.projects import ProjectsRepository


class ProjectService(
    IProjectService,
    GenericService[ProjectsRepository, ProjectIn, ProjectOut]
):
    """ ProjectService implementation. """
