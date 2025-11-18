from abc import ABC, abstractmethod
from typing import Literal

import httpx

HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]


class IServiceAdapter(ABC):
    def __init__(self, service_url: str):
        self.url = service_url

    @abstractmethod
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
    ) -> httpx.Response:
        """
        Basic wrapper for service calls.

        :param endpoint: endpoint of a specified service
        :param method: HTTP method for the new Request object
        :param params: Query parameters to include in the URL, as a string, dictionary, or sequence of two-tuples.
        :param content: Binary content to include in the body of the request, as bytes or a byte iterator.
        :param data: Form data to include in the body of the request, as a dictionary.
        :param json: A JSON serializable object to include in the body of the request.
        :param headers: Dictionary of HTTP headers to include in the request.
        :param cookies: Dictionary of Cookie items to include in the request.
        :return: response
        """


class BaseServiceAdapter(IServiceAdapter):
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
    ) -> httpx.Response:
        """ Real implementation of cross service calls. """

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.url}/{endpoint}",
                params=params,
                content=content,
                data=data,
                json=json,
                headers=headers,
                cookies=cookies,
            )
            response.raise_for_status()

        return response
