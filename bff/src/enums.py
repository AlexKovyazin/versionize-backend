from enum import Enum, IntEnum


class UserProjectRole(Enum):
    PM = "Руководитель проекта"
    PM_ASSISTANT = "Помощник руководителя проекта"
    DEVELOPER = "Разработчик раздела"
    CA_MANAGER = "Менеджер организации"
    EXPERT = "Эксперт"


class ProjectType(Enum):
    LINEAR = 1
    AREAL = 2


class DocumentStatuses(Enum):
    NEW = "Новый"
    IN_WORK = "В работе"
    READY_FOR_UPLOAD = "Готово к загрузке"
    PRIMARY_REMARKS = "Первичные замечания"
    REPEATED_REMARKS = "Повторные замечания"
    EXAMINATION = "Проверка экспертом"
    EXPIRED = "Просрочено"
    POSITIVE = "Положительное"
    NEGATIVE = "Отрицательное"


class DocumentContentType(Enum):
    PDF = "application/pdf"
    DOC = "application/msword"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return True if value in cls._value_set else False

    @classmethod
    def _value_set(cls):
        return {member.value for member in cls}


class NotificationType(IntEnum):
    PUSH = 1
    EMAIL = 2
    SMS = 3


class NotificationStatus(IntEnum):
    READ = 1
    UNREAD = 2
    SENT = 3
    CANCELED = 4


class NotificationPriority(IntEnum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
