from menu_sun_api.domain.model.pricing.pricing import Pricing
from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_integration.application.adapters.interfaces.abstract_domain_adapter import AbstractDomainAdapter
from menu_sun_integration.application.adapters.interfaces.abstract_get_adapter import AbstractGetAdapter
from menu_sun_integration.application.clients.interfaces.abstract_customer_pricing import AbstractCustomerPricingClient
from menu_sun_integration.application.translators.interfaces.abstract_customer_pricing_translator import \
    AbstractCustomerPricingTranslator
from menu_sun_integration.presentations.pricing.abstract_pricing_detail_get_response import \
    AbstractPricingDetailGetResponse
from menu_sun_integration.presentations.pricing.abstract_pricing_response import AbstractPricingResponse


class CustomerPricingAdapter(AbstractGetAdapter, AbstractDomainAdapter):
    def __init__(self, client: AbstractCustomerPricingClient, translator: AbstractCustomerPricingTranslator):
        self._client = client
        self._translator = translator

    def get_from_seller(self, customer: Customer) -> AbstractPricingDetailGetResponse:
        request = self._translator.to_seller_get_format(customer=customer)
        return self._client.get_customer_pricing(request)

    def get_domain(self, response: AbstractPricingResponse) -> Pricing:
        return self._translator.to_domain_format(response)


