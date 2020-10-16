from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.adapters.interfaces.abstract_domain_adapter import AbstractDomainAdapter
from menu_sun_integration.application.adapters.interfaces.abstract_get_adapter import AbstractGetAdapter
from menu_sun_integration.application.clients.interfaces.abstract_order_client import AbstractOrderClient
from menu_sun_integration.application.translators.interfaces.abstract_order_status_notification_translator import \
    AbstractOrderStatusNotificationTranslator
from menu_sun_integration.presentations.order.abstract_order_detail_get_response import AbstractOrderDetailGetResponse

from menu_sun_integration.presentations.order.abstract_order_status_notification_response import \
    AbstractOrderStatusNotificationResponse


class OrderStatusNotificationAdapter(AbstractGetAdapter, AbstractDomainAdapter):
    def __init__(self, client: AbstractOrderClient, translator: AbstractOrderStatusNotificationTranslator):
        self._client = client
        self._translator = translator

    def get_from_seller(self, order: Order) -> AbstractOrderDetailGetResponse:
        order = self._translator.to_seller_get_format(order)
        return self._client.get_order_status(order)

    def get_domain(self, response: AbstractOrderStatusNotificationResponse) -> Order:
        return self._translator.to_domain_format(response)
