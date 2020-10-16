import abc

from typing import Dict

from menu_sun_integration.presentations.order.abstract_order_detail_get_request import AbstractOrderDetailGetRequest
from menu_sun_integration.presentations.order.abstract_order_post_request import AbstractOrderPostRequest
from menu_sun_integration.presentations.order.abstract_order_status_notification_get_request import\
    AbstractOrderStatusNotificationGetRequest
from menu_sun_integration.presentations.order.abstract_order_status_put_request import AbstractOrderStatusPutRequest


class AbstractOrderRepository(abc.ABC):
    @abc.abstractmethod
    def post(self, request: AbstractOrderPostRequest) -> Dict:
        raise NotImplemented

    @abc.abstractmethod
    def get(self, request: AbstractOrderDetailGetRequest) -> Dict:
        raise NotImplemented

    def get_status(self, request: AbstractOrderStatusNotificationGetRequest) -> Dict:
        raise NotImplemented

    def put_order_status(self, request: AbstractOrderStatusPutRequest) -> Dict:
        raise NotImplemented
