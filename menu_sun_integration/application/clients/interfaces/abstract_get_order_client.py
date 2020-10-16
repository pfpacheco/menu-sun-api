import abc

from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.order.abstract_order_detail_get_request import AbstractOrderDetailGetRequest
from menu_sun_integration.presentations.order.abstract_order_detail_get_response import AbstractOrderDetailGetResponse


class AbstractGetOrderClient(AbstractClient):
    @abc.abstractmethod
    def get_order(self, request: AbstractOrderDetailGetRequest) -> AbstractOrderDetailGetResponse:
        raise NotImplementedError
