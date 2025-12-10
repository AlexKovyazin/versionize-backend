from notifications.src.adapters.orm import OrmNotification
from notifications.src.adapters.repositories.base import GenericRepository, INotificationsRepository
from notifications.src.domain.notification import NotificationIn


class NotificationsRepository(
    INotificationsRepository,
    GenericRepository[OrmNotification, NotificationIn]
):
    """ NotificationsRepository implementation. """
    ...
