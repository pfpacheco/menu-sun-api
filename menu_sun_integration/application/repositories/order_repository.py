from typing import Dict

from menu_sun_integration.application.context.ìnterfaces.abstract_get_post_context import AbstractGetPostContext
from menu_sun_integration.application.repositories.interfaces.abstract_order_repository import AbstractOrderRepository
from menu_sun_integration.presentations.order.abstract_order_detail_get_request import AbstractOrderDetailGetRequest
from menu_sun_integration.presentations.order.abstract_order_post_request import AbstractOrderPostRequest
from menu_sun_integration.presentations.order.abstract_order_status_notification_get_request import AbstractOrderStatusNotificationGetRequest
from menu_sun_integration.presentations.order.abstract_order_status_put_request import AbstractOrderStatusPutRequest


class OrderRepository(AbstractOrderRepository):
    def __init__(self, context: AbstractGetPostContext):
        self.context = context

    def post(self, request: AbstractOrderPostRequest) -> Dict:
        return self.context.post(request)

    def get(self, request: AbstractOrderDetailGetRequest) -> Dict:
        return self.context.get(request)

    def get_status(self, request: AbstractOrderStatusNotificationGetRequest) -> Dict:
        return self.context.get(request)

    def put_order_status(self, request: AbstractOrderStatusPutRequest) -> Dict:
        return self.context.put(request)
