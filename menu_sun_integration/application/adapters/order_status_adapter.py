from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.adapters.interfaces.abstract_domain_adapter import AbstractDomainAdapter
from menu_sun_integration.application.adapters.interfaces.abstract_get_adapter import AbstractGetAdapter
from menu_sun_integration.application.clients.interfaces.abstract_order_status_client import AbstractOrderStatusClient
from menu_sun_integration.application.translators.interfaces.abstract_order_status_translator import \
    AbstractOrderStatusTranslator
from menu_sun_integration.presentations.order.abstract_order_status_detail_put_response import \
    AbstractOrderStatusDetailPutResponse
from menu_sun_integration.presentations.order.abstract_order_status_put_response import AbstractOrderStatusPutResponse
from menu_sun_integration.presentations.order.order_status_sqs_platform import OrderStatusDetailSQSPlatform


class OrderStatusAdapter(AbstractGetAdapter, AbstractDomainAdapter):
    def __init__(self, client: AbstractOrderStatusClient, translator: AbstractOrderStatusTranslator):
        self._client = client
        self._translator = translator

    def get_from_seller(self, order: OrderStatusDetailSQSPlatform) -> AbstractOrderStatusDetailPutResponse:
        order = self._translator.to_seller_put_format(order)
        return self._client.put_order_status(order)

    def get_domain(self, response: AbstractOrderStatusPutResponse) -> Order:
        return self._translator.to_domain_format(response)
