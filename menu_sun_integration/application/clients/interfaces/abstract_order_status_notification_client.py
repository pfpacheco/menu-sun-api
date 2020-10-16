import abc

from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.order.abstract_order_status_notification_get_request import \
    AbstractOrderStatusNotificationGetRequest
from menu_sun_integration.presentations.order.abstract_order_status_notification_response import AbstractOrderStatusNotificationResponse


class AbstractOrderStatusNotificationClient(AbstractClient):
    @abc.abstractmethod
    def get_order_status(self, request: AbstractOrderStatusNotificationGetRequest) -> AbstractOrderStatusNotificationResponse:
        raise NotImplementedError
