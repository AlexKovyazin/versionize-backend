from enum import IntEnum


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
