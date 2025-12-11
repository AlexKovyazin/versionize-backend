import uuid

import httpx
import pytest
from fastapi import HTTPException
from httpx import HTTPStatusError

from bff.tests.fixtures import service_adapters
from bff.tests.fixtures.factories import ENTITY_FACTORIES


class BaseTestReadServiceAdapter:
    adapter_factory = None  # must be set in subclasses

    @pytest.fixture(autouse=True)
    def _setup_adapter(self):
        assert self.adapter_factory is not None
        self.service_adapter = self.adapter_factory()

    async def test_get(self):
        factory = ENTITY_FACTORIES.get(self.service_adapter.out_schema)
        awaitable_entity = factory.build()
        response_entity = await self.service_adapter.get(
            awaitable_entity.id,
            response_entity=awaitable_entity.model_dump(mode="json")
        )

        assert response_entity == awaitable_entity

    async def test_get_404(self):
        with pytest.raises(HTTPException) as exc_info:
            await self.service_adapter.get(
                uuid.uuid4(),
                raise_error=httpx.codes.NOT_FOUND
            )

        assert exc_info.value.status_code == httpx.codes.NOT_FOUND

    @pytest.mark.parametrize(
        "error_code",
        [
            e for e in httpx.codes
            if e.is_error(e) and not e.value == 404
        ]
    )
    async def test_get_any_exception(self, error_code: httpx.codes):
        with pytest.raises(HTTPStatusError) as exc_info:
            await self.service_adapter.get(
                uuid.uuid4(),
                raise_error=error_code
            )

        assert exc_info.value.response.status_code == error_code

    @pytest.mark.parametrize("entities_amount", [0, 1, 2])
    async def test_list(self, entities_amount: int):
        factory = ENTITY_FACTORIES.get(self.service_adapter.out_schema)
        awaitable_entities = factory.batch(entities_amount)
        search_params = self.service_adapter.search_params()

        response_entities = await self.service_adapter.list(
            search_params,
            response_entity=[e.model_dump(mode="json") for e in awaitable_entities]
        )

        assert awaitable_entities == response_entities


class TestCompaniesReadServiceAdapter(BaseTestReadServiceAdapter):
    adapter_factory = service_adapters.FakeCompaniesReadServiceAdapter


class TestDocumentsReadServiceAdapter(BaseTestReadServiceAdapter):
    adapter_factory = service_adapters.FakeDocumentsReadServiceAdapter


class TestNotificationsReadServiceAdapter(BaseTestReadServiceAdapter):
    adapter_factory = service_adapters.FakeNotificationsReadServiceAdapter


class TestProjectsReadServiceAdapter(BaseTestReadServiceAdapter):
    adapter_factory = service_adapters.FakeProjectsReadServiceAdapter


class TestRemarksReadServiceAdapter(BaseTestReadServiceAdapter):
    adapter_factory = service_adapters.FakeRemarksReadServiceAdapter


class TestRemarkDocsReadServiceAdapter(BaseTestReadServiceAdapter):
    adapter_factory = service_adapters.FakeRemarkDocsReadServiceAdapter


class TestDefaultSectionsReadServiceAdapter(BaseTestReadServiceAdapter):
    adapter_factory = service_adapters.FakeDefaultSectionsReadServiceAdapter


class TestSectionsReadServiceAdapter(BaseTestReadServiceAdapter):
    adapter_factory = service_adapters.FakeSectionsReadServiceAdapter


class TestUsersReadServiceAdapter(BaseTestReadServiceAdapter):
    adapter_factory = service_adapters.FakeProjectsReadServiceAdapter
