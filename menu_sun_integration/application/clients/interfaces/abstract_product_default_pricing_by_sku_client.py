import abc

from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.inventory.abstract_inventory_get_response import AbstractInventoryGetResponse
from menu_sun_integration.presentations.pricing.abstract_pricing_detail_get_response import \
    AbstractPricingDetailGetResponse
from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_by_sku_post_request import \
    AbstractProductDefaultPricingBySkuPostRequest


class AbstractProductDefaultPricingBySkuClient(AbstractClient):
    @abc.abstractmethod
    def get_price(self, request: AbstractProductDefaultPricingBySkuPostRequest) -> AbstractPricingDetailGetResponse:
        raise NotImplemented
