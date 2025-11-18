from uuid import UUID

from nats.js.api import PubAck

from bff.src.adapters.base import BaseServiceAdapter
from bff.src.adapters.broker import cmd
from bff.src.adapters.broker.nats import NatsJS, Streams
from bff.src.config.logging import request_id_var
from bff.src.domain.project import ProjectOut, ProjectsSearchParams, ProjectIn, ProjectUpdate


class ProjectServiceAdapter(BaseServiceAdapter):

    def __init__(self, service_url: str, broker):
        super().__init__(service_url)
        self.broker: NatsJS = broker

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

    async def create(self, data: ProjectIn) -> PubAck:
        return await self.broker.publish(
            data,
            cmd.CREATE_PROJECT,
            headers={"correlation_id": request_id_var.get()},
            stream=Streams.CMD
        )

    async def update(self, data: ProjectUpdate) -> PubAck:
        return await self.broker.publish(
            data.model_dump_json(),
            cmd.UPDATE_PROJECT,
            headers={"correlation_id": request_id_var.get()},
            stream=Streams.CMD
        )

    async def delete(self, project_id: UUID) -> PubAck:
        return await self.broker.publish(
            str(project_id),
            cmd.DELETE_PROJECT,
            headers={"correlation_id": request_id_var.get()},
            stream=Streams.CMD
        )
