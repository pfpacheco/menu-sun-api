import abc

from menu_sun_integration.application.adapters.order_status_notification_adapter import OrderStatusNotificationAdapter
from menu_sun_integration.application.services.interfaces.abstract_service import AbstractService


class AbstractOrderStatusNotificationService(AbstractService):
    _adapter: OrderStatusNotificationAdapter = None

    @abc.abstractmethod
    def get_status_order_from_seller(self) -> None:
        raise NotImplementedError
