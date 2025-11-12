from uuid import UUID

from bff.src.adapters.base import BaseServiceAdapter
from bff.src.domain.project import ProjectOut, ProjectsSearchParams


class ProjectServiceAdapter(BaseServiceAdapter):
    async def get_project(
            self,
            project_id: UUID
    ) -> ProjectOut:
        response = await self._make_request(f"projects/{project_id}")
        return ProjectOut.model_validate(response.json())

    async def get_many_projects(
            self,
            filter_data: ProjectsSearchParams
    ) -> list[ProjectOut]:
        response = await self._make_request(
            "projects",
            params=filter_data.model_dump(exclude_none=True)
        )
        return [ProjectOut.model_validate(p) for p in response.json()]
