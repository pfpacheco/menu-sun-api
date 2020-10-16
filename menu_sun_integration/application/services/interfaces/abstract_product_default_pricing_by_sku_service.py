import abc

from menu_sun_integration.application.adapters.product_default_pricing_adapter import ProductDefaultPricingAdapter
from menu_sun_integration.application.adapters.product_default_pricing_by_sku_adapter import \
    ProductDefaultPricingBySkuAdapter
from menu_sun_integration.application.services.interfaces.abstract_service import AbstractService


class AbstractProductDefaultPricingBySkuService(AbstractService):
    _adapter: ProductDefaultPricingBySkuAdapter = None

    @abc.abstractmethod
    def update_price_from_seller(self) -> None:
        raise NotImplementedError
