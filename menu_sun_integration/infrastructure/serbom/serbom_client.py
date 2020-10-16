import json
import xmltodict

from menu_sun_integration.application.clients.interfaces.abstract_post_order_client import AbstractPostOrderClient
from menu_sun_integration.application.clients.interfaces.abstract_product_default_pricing_client import \
    AbstractProductDefaultPricingClient
from menu_sun_integration.application.repositories.interfaces.abstract_order_repository import AbstractOrderRepository
from menu_sun_integration.application.repositories.interfaces.abstract_product_repository import \
    AbstractProductRepository
from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_request import \
    SerbomOrderPostOrderRequest
from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_response import \
    SerbomOrderPostResponse
from menu_sun_integration.infrastructure.serbom.presentations.pricing.serbom_pricing_detail_get_response import \
    SerbomPricingDetailGetResponse
from menu_sun_integration.infrastructure.serbom.presentations.pricing.product.\
    serbom_product_default_pricing_detail_get_request import SerbomProductDefaultPricingDetailGetRequest


class SerbomClient(AbstractPostOrderClient, AbstractProductDefaultPricingClient):

    def __init__(self, product_repository: AbstractProductRepository, order_repository: AbstractOrderRepository):
        super().__init__()
        self.product_repository = product_repository
        self.order_repository = order_repository

    def post_order(self, request: SerbomOrderPostOrderRequest) -> SerbomOrderPostResponse:
        data = self.order_repository.post(request)
        return SerbomOrderPostResponse(payload=json.dumps(xmltodict.parse(data)))

    def get_products_default_pricing(self, request: SerbomProductDefaultPricingDetailGetRequest) -> \
            SerbomPricingDetailGetResponse:
        data = self.product_repository.get_prices(request)
        return SerbomPricingDetailGetResponse(payload=data)
