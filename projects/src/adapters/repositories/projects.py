from projects.src.adapters.orm import OrmProject
from projects.src.adapters.repositories.base import GenericRepository, IProjectsRepository
from projects.src.domain.project import ProjectIn


class ProjectsRepository(
    IProjectsRepository,
    GenericRepository[OrmProject, ProjectIn]
):
    """ ProjectsRepository implementation. """
    ...
