from notifications.src.service.base import GenericService, INotificationService
from notifications.src.domain.notification import NotificationIn, NotificationOut
from notifications.src.adapters.repositories.notifications import NotificationsRepository


class NotificationService(
    INotificationService,
    GenericService[NotificationsRepository, NotificationIn, NotificationOut]
):
    """ NotificationService implementation. """
