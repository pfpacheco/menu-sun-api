import abc

from typing import Dict

from menu_sun_integration.presentations.pricing.customer.abstract_customer_pricing_detail_get_request import \
    AbstractCustomerPricingDetailGetRequest


class AbstractPricingRepository(abc.ABC):
    @abc.abstractmethod
    def get_by_customer(self, request: AbstractCustomerPricingDetailGetRequest) -> Dict:
        raise NotImplemented
