from enum import Enum


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
