import abc

from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator
from menu_sun_integration.presentations.order.abstract_order_status_notification_get_request import AbstractOrderStatusNotificationGetRequest
from menu_sun_integration.presentations.order.abstract_order_status_notification_response import AbstractOrderStatusNotificationResponse


class AbstractOrderStatusNotificationTranslator(AbstractTranslator):
    @abc.abstractmethod
    def to_seller_get_format(self, entity: Order) -> AbstractOrderStatusNotificationGetRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_domain_format(self, response: AbstractOrderStatusNotificationResponse) -> Order:
        raise NotImplementedError
