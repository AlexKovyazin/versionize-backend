from enum import Enum


# TODO эти статусы должны быть у Sections, а не у Documents.
#  Для документов должны быть статусы:
#  - NEW
#  - READY_FOR_UPLOAD
#  - EXAMINATION
#  - POSITIVE
#  - NEGATIVE
#  При этом по повторяющимся статусам должно быть настроено событие
#  взаимного изменения статусов у раздела и документа
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


class UserProjectRole(Enum):
    PM = "Руководитель проекта"
    PM_ASSISTANT = "Помощник руководителя проекта"
    DEVELOPER = "Разработчик раздела"
    CA_MANAGER = "Менеджер организации"
    EXPERT = "Эксперт"


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
