import abc

from menu_sun_integration.application.clients.interfaces.abstract_get_order_client import AbstractGetOrderClient
from menu_sun_integration.application.clients.interfaces.abstract_post_order_client import AbstractPostOrderClient
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.order.abstract_order_detail_get_request import AbstractOrderDetailGetRequest
from menu_sun_integration.presentations.order.abstract_order_detail_get_response import AbstractOrderDetailGetResponse
from menu_sun_integration.presentations.order.abstract_order_post_response import AbstractOrderPostResponse
from menu_sun_integration.presentations.order.abstract_order_status_notification_get_request import \
    AbstractOrderStatusNotificationGetRequest
from menu_sun_integration.presentations.order.abstract_order_status_put_request import AbstractOrderStatusPutRequest
from menu_sun_integration.presentations.order.abstract_order_status_put_response import AbstractOrderStatusPutResponse


class AbstractOrderClient(AbstractGetOrderClient, AbstractPostOrderClient):
    @abc.abstractmethod
    def get_order(self, request: AbstractOrderDetailGetRequest) -> AbstractOrderDetailGetResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def post_order(self, request: AbstractRequest) -> AbstractOrderPostResponse:
        raise NotImplementedError

    def get_order_status(self, request: AbstractOrderStatusNotificationGetRequest) -> AbstractOrderDetailGetResponse:
        raise NotImplementedError

    def put_order_status(self, request: AbstractOrderStatusPutRequest) -> AbstractOrderStatusPutResponse:
        raise NotImplementedError
