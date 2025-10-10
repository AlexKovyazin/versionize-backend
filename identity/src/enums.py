from enum import Enum


class UserProjectRole(Enum):
    PM = "Руководитель проекта"
    PM_ASSISTANT = "Помощник руководителя проекта"
    DEVELOPER = "Разработчик раздела"
    CA_MANAGER = "Менеджер организации"
    EXPERT = "Эксперт"
