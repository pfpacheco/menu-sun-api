import abc

from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator
from menu_sun_integration.presentations.order.abstract_order_status_put_request import AbstractOrderStatusPutRequest
from menu_sun_integration.presentations.order.abstract_order_status_put_response import AbstractOrderStatusPutResponse
from menu_sun_integration.presentations.order.order_status_sqs_platform import OrderStatusDetailSQSPlatform


class AbstractOrderStatusTranslator(AbstractTranslator):
    @abc.abstractmethod
    def to_seller_put_format(self, order: OrderStatusDetailSQSPlatform) -> AbstractOrderStatusPutRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_domain_format(self, response: AbstractOrderStatusPutResponse) -> Order:
        raise NotImplementedError
