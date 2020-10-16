import abc

from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.order.abstract_order_detail_get_request import AbstractOrderDetailGetRequest
from menu_sun_integration.presentations.order.abstract_order_response import AbstractOrderResponse


class AbstractOrderTranslator(AbstractTranslator):
    @abc.abstractmethod
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_seller_get_format(self, entity: Order) -> AbstractOrderDetailGetRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_domain_format(self, response: AbstractOrderResponse) -> Order:
        raise NotImplementedError


