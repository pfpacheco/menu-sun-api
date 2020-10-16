import abc

from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.pricing.abstract_pricing_detail_get_response import \
    AbstractPricingDetailGetResponse
from menu_sun_integration.presentations.pricing.customer.abstract_customer_pricing_detail_get_request import \
    AbstractCustomerPricingDetailGetRequest


class AbstractCustomerPricingClient(AbstractClient):
    @abc.abstractmethod
    def get_customer_pricing(self, request: AbstractCustomerPricingDetailGetRequest) -> AbstractPricingDetailGetResponse:
        raise NotImplementedError

