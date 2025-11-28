from dataclasses import dataclass


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


@dataclass(frozen=True)
class BaseEvents:
    """
    Base dataclass for C(r)UD events.

    Implements Create, Update, Delete properties with correct command subjects.
    """

    service_name: str
    entity_name: str

    @property
    def created(self) -> str:
        return f"cmd.{self.service_name}.{self.entity_name}Created"

    @property
    def updated(self) -> str:
        return f"cmd.{self.service_name}.{self.entity_name}Updated"

    @property
    def deleted(self) -> str:
        return f"cmd.{self.service_name}.{self.entity_name}Deleted"


@dataclass(frozen=True)
class ProjectEventsExtra:
    """ Example dataclass for extra commands. """

    example: str = f"cmd.project.ExtraEvent"


@dataclass(frozen=True, slots=True)
class ProjectEvents(Singleton, ProjectEventsExtra, BaseEvents):
    """ Implements all Project entity commands. """
