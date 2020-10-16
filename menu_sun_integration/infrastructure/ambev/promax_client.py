from menu_sun_integration.application.clients.interfaces.abstract_get_order_client import AbstractGetOrderClient
from menu_sun_integration.application.clients.interfaces.abstract_post_order_client import AbstractPostOrderClient
from menu_sun_integration.application.repositories.interfaces.abstract_order_repository import AbstractOrderRepository
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_detail_get_request import \
    PromaxOrderDetailGetRequest
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_detail_get_response import \
    PromaxOrderDetailGetResponse
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_post_request import \
    PromaxOrderPostRequest
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_post_response import \
    PromaxOrderPostResponse


class PromaxClient(AbstractPostOrderClient, AbstractGetOrderClient):
    def __init__(self, order_repository: AbstractOrderRepository):
        super().__init__()
        self.order_repository = order_repository

    def post_order(self, request: PromaxOrderPostRequest) -> PromaxOrderPostResponse:
        data = self.order_repository.post(request)
        return PromaxOrderPostResponse(payload=data)

    def get_order(self, request: PromaxOrderDetailGetRequest) -> PromaxOrderDetailGetResponse:
        data = self.order_repository.get(request)
        return PromaxOrderDetailGetResponse(order_id=request.order_id, payload=data)
