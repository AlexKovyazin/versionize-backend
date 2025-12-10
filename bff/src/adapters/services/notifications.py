from bff.src.adapters.broker.cmd import ProjectCmd
from bff.src.adapters.services.base import GenericServiceReadAdapter, GenericServiceWriteAdapter
from bff.src.adapters.services.base import INotificationsReadServiceAdapter, INotificationsWriteServiceAdapter
from bff.src.domain.notification import NotificationIn, NotificationUpdate
from bff.src.domain.notification import NotificationsSearch, NotificationOut


class NotificationsReadServiceAdapter(
    INotificationsReadServiceAdapter,
    GenericServiceReadAdapter[NotificationsSearch, NotificationOut]
):
    ...


class NotificationsWriteServiceAdapter(
    INotificationsWriteServiceAdapter,
    GenericServiceWriteAdapter[ProjectCmd, NotificationIn, NotificationUpdate]
):
    ...
