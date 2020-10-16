from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.adapters.interfaces.abstract_domain_adapter import AbstractDomainAdapter
from menu_sun_integration.application.adapters.interfaces.abstract_get_adapter import AbstractGetAdapter
from menu_sun_integration.application.adapters.interfaces.abstract_post_adapter import AbstractSendAdapter
from menu_sun_integration.application.clients.interfaces.abstract_order_client import AbstractOrderClient
from menu_sun_integration.application.translators.interfaces.abstract_order_translator import AbstractOrderTranslator
from menu_sun_integration.presentations.order.abstract_order_detail_get_response import AbstractOrderDetailGetResponse
from menu_sun_integration.presentations.order.abstract_order_platform import AbstractOrderPlatform
from menu_sun_integration.presentations.order.abstract_order_post_response import AbstractOrderPostResponse
from menu_sun_integration.presentations.order.abstract_order_response import AbstractOrderResponse


class OrderAdapter(AbstractSendAdapter, AbstractGetAdapter, AbstractDomainAdapter):
    def __init__(self, client: AbstractOrderClient, translator: AbstractOrderTranslator):
        self._client = client
        self._translator = translator

    def send_to_seller(self, order_platform: AbstractOrderPlatform) -> AbstractOrderPostResponse:
        order = self._translator.to_seller_send_format(order_platform)
        return self._client.post_order(order)

    def get_from_seller(self, order: Order) -> AbstractOrderDetailGetResponse:
        order = self._translator.to_seller_get_format(order)
        return self._client.get_order(order)

    def get_domain(self, response: AbstractOrderResponse) -> Order:
        return self._translator.to_domain_format(response)
