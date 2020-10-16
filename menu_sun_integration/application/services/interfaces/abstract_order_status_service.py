import abc

from menu_sun_api.domain import Default
from menu_sun_integration.application.adapters.order_status_adapter import OrderStatusAdapter
from menu_sun_integration.application.services.interfaces.abstract_service import AbstractService
from menu_sun_integration.presentations.order.abstract_order_status_put_response \
    import AbstractOrderStatusPutResponse


class AbstractOrderStatusService(AbstractService):
    _adapter: OrderStatusAdapter

    @abc.abstractmethod
    def put_orders_to_seller(self) -> None:
        raise NotImplementedError
