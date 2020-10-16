import abc

from menu_sun_integration.application.adapters.product_default_pricing_adapter import ProductDefaultPricingAdapter
from menu_sun_integration.application.services.interfaces.abstract_service import AbstractService


class AbstractProductDefaultPricingService(AbstractService):
    _adapter: ProductDefaultPricingAdapter = None

    @abc.abstractmethod
    def update_product_default_pricing_from_seller(self) -> None:
        raise NotImplementedError
