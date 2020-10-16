

import abc

from typing import Dict

from menu_sun_integration.presentations.inventory.abstract_inventory_by_sku_post_request import \
    AbstractInventoryBySkuPostRequest
from menu_sun_integration.presentations.inventory.abstract_inventory_get_request import AbstractInventoryGetRequest
from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_by_sku_post_request import \
    AbstractProductDefaultPricingBySkuPostRequest
from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_detail_get_request import \
    AbstractProductDefaultPricingDetailGetRequest
from menu_sun_integration.presentations.product.abstract_product_get_request import AbstractProductGetRequest


class AbstractProductRepository(abc.ABC):
    @abc.abstractmethod
    def get_all(self, request: AbstractProductGetRequest) -> Dict:
        raise NotImplemented

    @abc.abstractmethod
    def get_inventories(self, request: AbstractInventoryGetRequest) -> Dict:
        raise NotImplemented

    @abc.abstractmethod
    def get_prices(self, request: AbstractProductDefaultPricingDetailGetRequest) -> Dict:
        raise NotImplemented

    @abc.abstractmethod
    def get_inventory(self, request: AbstractInventoryBySkuPostRequest) -> Dict:
        raise NotImplemented

    @abc.abstractmethod
    def get_price(self, request: AbstractProductDefaultPricingBySkuPostRequest) -> Dict:
        raise NotImplemented
