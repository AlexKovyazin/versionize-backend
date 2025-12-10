from typing import AsyncIterable

from dishka import provide, Scope, Provider

from notifications.src.adapters.repositories.notifications import NotificationsRepository
from notifications.src.service.notification import NotificationService
from notifications.src.service.uow import UnitOfWork


class DependencyProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_uow(self) -> AsyncIterable[UnitOfWork]:
        """ Real dependency of UnitOfWork for production. """
        async with UnitOfWork() as uow:
            yield uow

    @provide(scope=Scope.REQUEST)
    async def get_notifications_repository(
            self,
            uow: UnitOfWork
    ) -> NotificationsRepository:
        """ Real dependency of NotificationsRepository for production. """
        return NotificationsRepository(uow=uow)

    @provide(scope=Scope.REQUEST)
    async def get_notification_service(
            self,
            repo: NotificationsRepository,
    ) -> NotificationService:
        """ Real dependency of NotificationService for production. """
        return NotificationService(repo)
