import traceback
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TypeAlias, Sequence, Any

from nats.aio.client import Client
from nats.js import JetStreamContext
from pydantic import BaseModel, TypeAdapter

from bff.src.config.logging import logger
from bff.src.config.settings import settings

JsonDecodable: TypeAlias = bool | bytes | bytearray | float | int | str | None
SendableArray: TypeAlias = Sequence["SendableMessage"]
SendableMessage: TypeAlias = (
        JsonDecodable
        | Decimal
        | datetime
        | BaseModel
        | SendableArray
        | None
)


class Streams(Enum):
    CMD = "cmd"
    EVENTS = "events"


class NatsJS:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.server = settings.nats_url
        self.nc: Client = Client()
        self.js: JetStreamContext = self.nc.jetstream()
        self._connected = False
        self._streams = tuple([s.value for s in Streams])
        self._initialized = True

    def __bool__(self) -> bool:
        return self._connected

    async def connect(self) -> None:
        if not self._connected:
            await self.nc.connect(
                self.server,
                error_cb=self.error_cb,
                reconnected_cb=self.reconnected_cb,
                disconnected_cb=self.disconnected_cb,
                closed_cb=self.closed_cb,
            )

        self._connected = True

    async def disconnect(self) -> None:
        if self._connected:
            await self.nc.close()

        self.nc = None
        self.js = None
        self._connected = False

    async def publish(
            self,
            message: SendableMessage,
            subject: str,
            stream: Streams | None = None,
            headers: dict[str, Any] | None = None,
            msg_ttl: float | None = None,
            timeout: float | None = None,
    ) -> None:

        if not isinstance(stream, Streams):
            raise ValueError("stream arg must be an instance of Streams")
        if not subject.startswith(self._streams):
            raise ValueError("Invalid subject. Subject must start with stream name")

        adapter = TypeAdapter(type(message))
        prepared_msg = adapter.dump_json(message)
        await self.js.publish(
            subject,
            prepared_msg,
            stream=stream.value,
            headers=headers,
            msg_ttl=msg_ttl,
            timeout=timeout,
        )

    @classmethod
    async def disconnected_cb(cls):
        logger.warning("Disconnected from NATS server")

    @classmethod
    async def reconnected_cb(cls):
        logger.warning("Reconnected to NATS server")

    @classmethod
    async def error_cb(cls, e):
        logger.error(f"NATS {type(e).__name__}: {traceback.format_exc()}")

    @classmethod
    async def closed_cb(cls):
        logger.info("NATS connection is closed")
