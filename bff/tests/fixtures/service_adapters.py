from typing import TypeVar
from uuid import UUID

import httpx
from httpx import Request
from pydantic import BaseModel

from bff.src.adapters.services import base as base_adapters
from bff.src.adapters.services.base import GenericServiceReadAdapter, IServiceAdapter
from bff.src.adapters.services.base import HttpMethod
from bff.src.config.logging import request_id_var
from bff.src.domain import company, document, notification, project, remark, remark_doc, section, user, s3

OUT_SCHEMA = TypeVar("OUT_SCHEMA", bound=BaseModel)
SEARCH_PARAMS = TypeVar("SEARCH_PARAMS", bound=BaseModel)


class FakeBaseServiceAdapter(
    IServiceAdapter
):
    async def _make_request(
            self,
            endpoint: str,
            method: HttpMethod = "GET",
            params: dict = None,
            content: bytes = None,
            data: dict = None,
            json: dict | list = None,
            headers: dict = None,
            cookies: dict = None,
            # test options:
            response_entity: dict = None,
            raise_error: httpx.codes = None
    ) -> httpx.Response:
        """
        Mock implementation of cross service calls.
        """

        request_headers = {
            "X-Request-ID": request_id_var.get(""),
            **(headers or {}),
        }
        mock_request = Request(
            method,
            f"{self.url}/{endpoint}",
            params=params,
            content=content,
            data=data,
            json=json,
            headers=request_headers,
            cookies=cookies,
        )
        mock_response = httpx.Response(
            status_code=httpx.codes.OK,
            headers=request_headers,
            json=response_entity,
            request=mock_request
        )
        if raise_error:
            mock_response.status_code = raise_error

        mock_response.raise_for_status()

        return mock_response


class FakeGenericServiceReadAdapter(
    FakeBaseServiceAdapter,
    GenericServiceReadAdapter[SEARCH_PARAMS, OUT_SCHEMA],
):
    """ Class with mocked http request. """


# Implementations:

class FakeCompaniesReadServiceAdapter(
    base_adapters.ICompaniesReadServiceAdapter,
    FakeGenericServiceReadAdapter[company.CompaniesSearch, company.Company]
):
    """ Fake companies read service adapter implementation. """


class FakeDocumentsReadServiceAdapter(
    base_adapters.IDocumentsReadServiceAdapter,
    FakeGenericServiceReadAdapter[document.DocumentsSearch, document.DocumentOut]
):
    """ Fake documents read service adapter implementation. """

    async def get_download_url(self, document_id: UUID, **kwargs) -> s3.S3DownloadResponse:
        raise NotImplementedError()

    async def get_upload_url(self, document_id: UUID, **kwargs) -> s3.S3UploadResponse:
        raise NotImplementedError()


class FakeNotificationsReadServiceAdapter(
    base_adapters.INotificationsReadServiceAdapter,
    FakeGenericServiceReadAdapter[notification.NotificationsSearch, notification.NotificationOut]
):
    """ Fake notifications read service adapter implementation. """


class FakeProjectsReadServiceAdapter(
    base_adapters.IProjectsReadServiceAdapter,
    FakeGenericServiceReadAdapter[project.ProjectsSearchParams, project.ProjectOut]
):
    """ Fake projects read service adapter implementation. """


class FakeRemarksReadServiceAdapter(
    base_adapters.IRemarksReadServiceAdapter,
    FakeGenericServiceReadAdapter[remark.RemarksSearch, remark.RemarkOut]
):
    """ Fake remarks read service adapter implementation. """


class FakeRemarkDocsReadServiceAdapter(
    base_adapters.IRemarkDocsReadServiceAdapter,
    FakeGenericServiceReadAdapter[remark_doc.RemarkDocsSearch, remark_doc.RemarkDocOut]
):
    """ Fake remark docs read service adapter implementation. """


class FakeDefaultSectionsReadServiceAdapter(
    base_adapters.IDefaultSectionsReadServiceAdapter,
    FakeGenericServiceReadAdapter[section.DefaultSectionsSearch, section.DefaultSectionOut]
):
    """ Fake default sections read service adapter implementation. """


class FakeSectionsReadServiceAdapter(
    base_adapters.ISectionsReadServiceAdapter,
    FakeGenericServiceReadAdapter[section.SectionsSearch, section.SectionOut]
):
    """ Fake sections read service adapter implementation. """


class FakeUsersReadServiceAdapter(
    base_adapters.IUsersReadServiceAdapter,
    FakeGenericServiceReadAdapter[user.UsersSearch, user.User]
):
    """ Fake users read service adapter implementation. """
