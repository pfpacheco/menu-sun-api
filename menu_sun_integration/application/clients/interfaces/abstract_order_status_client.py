import abc

from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.order.abstract_order_status_detail_put_response import \
    AbstractOrderStatusDetailPutResponse
from menu_sun_integration.presentations.order.abstract_order_status_put_request import AbstractOrderStatusPutRequest


class AbstractOrderStatusClient(AbstractClient):
    @abc.abstractmethod
    def put_order_status(self, request: AbstractOrderStatusPutRequest) -> AbstractOrderStatusDetailPutResponse:
        raise NotImplementedError
