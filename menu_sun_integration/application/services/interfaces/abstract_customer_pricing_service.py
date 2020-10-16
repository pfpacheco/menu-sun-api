import abc

from menu_sun_integration.application.adapters.customer_pricing_adapter import CustomerPricingAdapter
from menu_sun_integration.application.services.interfaces.abstract_service import AbstractService


class AbstractPricingByCustomerService(AbstractService):
    _adapter: CustomerPricingAdapter = None

    @abc.abstractmethod
    def update_customer_pricing_from_seller(self) -> None:
        raise NotImplementedError
