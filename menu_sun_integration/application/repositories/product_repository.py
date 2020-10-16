from typing import Dict

from menu_sun_integration.application.context.ìnterfaces.abstract_get_post_context import AbstractGetPostContext
from menu_sun_integration.application.repositories.interfaces.abstract_product_repository import \
    AbstractProductRepository
from menu_sun_integration.presentations.inventory.abstract_inventory_by_sku_post_request import \
    AbstractInventoryBySkuPostRequest
from menu_sun_integration.presentations.inventory.abstract_inventory_get_request import AbstractInventoryGetRequest
from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_by_sku_post_request import \
    AbstractProductDefaultPricingBySkuPostRequest
from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_detail_get_request import \
    AbstractProductDefaultPricingDetailGetRequest
from menu_sun_integration.presentations.product.abstract_product_get_request import AbstractProductGetRequest


class ProductRepository(AbstractProductRepository):
    def __init__(self, context: AbstractGetPostContext):
        self.context = context

    def get_all(self, request: AbstractProductGetRequest) -> Dict:
        return self.context.get(request)

    def get_inventories(self, request: AbstractInventoryGetRequest) -> Dict:
        return self.context.get(request)

    def get_prices(self, request: AbstractProductDefaultPricingDetailGetRequest) -> Dict:
        return self.context.get(request)

    def get_inventory(self, request: AbstractInventoryBySkuPostRequest) -> Dict:
        return self.context.post(request)

    def get_price(self, request: AbstractProductDefaultPricingBySkuPostRequest) -> Dict:
        return self.context.post(request)
