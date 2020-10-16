import abc

from menu_sun_api.domain import Default
from menu_sun_integration.application.adapters.order_adapter import OrderAdapter
from menu_sun_integration.application.services.interfaces.abstract_service import AbstractService
from menu_sun_integration.presentations.order.abstract_order_detail_get_response import AbstractOrderDetailGetResponse


class AbstractOrderService(AbstractService):
    _adapter: OrderAdapter

    @abc.abstractmethod
    def post_orders_to_seller(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_order_from_seller(self, order: Default) -> AbstractOrderDetailGetResponse:
        raise NotImplementedError
