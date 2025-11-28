from abc import ABC, abstractmethod

from bff.src.adapters.broker.types import SendableMessage


class IBroker(ABC):
    _instance = None

    @abstractmethod
    async def connect(self):
        """ Connect to the broker. """

    @abstractmethod
    async def disconnect(self):
        """ Disconnect from the broker. """

    @abstractmethod
    async def publish(self, message: SendableMessage, subject: str, **kwargs):
        """ Publish message to subject."""

    @classmethod
    async def disconnected_cb(cls):
        """ Callback on disconnecting. """

    @classmethod
    async def reconnected_cb(cls):
        """ Callback on reconnecting. """

    @classmethod
    async def error_cb(cls, e):
        """ Callback on error. """

    @classmethod
    async def closed_cb(cls):
        """ Callback on closed connection. """
