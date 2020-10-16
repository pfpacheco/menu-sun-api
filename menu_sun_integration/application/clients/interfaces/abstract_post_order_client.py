import abc

from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.order.abstract_order_post_response import AbstractOrderPostResponse


class AbstractPostOrderClient(AbstractClient):
    @abc.abstractmethod
    def post_order(self, request: AbstractRequest) -> AbstractOrderPostResponse:
        raise NotImplementedError
