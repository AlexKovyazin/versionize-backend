from dataclasses import dataclass


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


@dataclass(frozen=True)
class BaseCmd:
    """
    Base dataclass for C(r)UD commands.

    Implements Create, Update, Delete properties with correct command subjects.
    """

    service_name: str
    entity_name: str

    @property
    def create(self) -> str:
        return f"cmd.{self.service_name}.Create{self.entity_name}"

    @property
    def update(self) -> str:
        return f"cmd.{self.service_name}.Update{self.entity_name}"

    @property
    def delete(self) -> str:
        return f"cmd.{self.service_name}.Delete{self.entity_name}"


@dataclass(frozen=True, slots=True)
class RemarkCmd(Singleton, BaseCmd):
    """ Implements all Remark entity commands. """


@dataclass(frozen=True, slots=True)
class RemarkDocCmd(Singleton, BaseCmd):
    """ Implements all Remark entity commands. """
