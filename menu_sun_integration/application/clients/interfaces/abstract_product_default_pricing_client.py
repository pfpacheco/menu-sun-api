import abc

from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.pricing.abstract_pricing_detail_get_response import \
    AbstractPricingDetailGetResponse
from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_detail_get_request import \
    AbstractProductDefaultPricingDetailGetRequest


class AbstractProductDefaultPricingClient(AbstractClient):
    @abc.abstractmethod
    def get_products_default_pricing(self, request: AbstractProductDefaultPricingDetailGetRequest) \
            -> AbstractPricingDetailGetResponse:
        raise NotImplementedError
