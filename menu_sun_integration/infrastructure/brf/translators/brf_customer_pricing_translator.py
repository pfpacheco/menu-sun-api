from menu_sun_api.domain.model.pricing.pricing import Pricing
from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_integration.application.translators.interfaces.abstract_customer_pricing_translator import \
    AbstractCustomerPricingTranslator
from menu_sun_integration.infrastructure.brf.presentations.pricing.brf_pricing_response import BRFPricingResponse
from menu_sun_integration.infrastructure.brf.presentations.pricing.customer.brf_customer_pricing_detail_get_request \
    import BRFCustomerPricingDetailGetRequest
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.pricing.customer.abstract_customer_pricing_detail_get_request import \
    AbstractCustomerPricingDetailGetRequest


class BRFCustomerPricingTranslator(AbstractCustomerPricingTranslator):
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    def to_seller_get_format(self, customer: Customer) -> AbstractCustomerPricingDetailGetRequest:
        return BRFCustomerPricingDetailGetRequest(postal_code=customer.cep, document=customer.document)

    def to_domain_format(self, response: BRFPricingResponse) -> [Pricing]:
        return self.bind_pricing(response)
