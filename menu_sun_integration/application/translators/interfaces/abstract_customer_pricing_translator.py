import abc

from menu_sun_api.domain.model.pricing.pricing import Pricing
from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.pricing.abstract_pricing_response import AbstractPricingResponse
from menu_sun_integration.presentations.pricing.customer.abstract_customer_pricing_detail_get_request import \
    AbstractCustomerPricingDetailGetRequest


class AbstractCustomerPricingTranslator(AbstractTranslator):
    @abc.abstractmethod
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_seller_get_format(self, customer: Customer) -> AbstractCustomerPricingDetailGetRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_domain_format(self, response: AbstractPricingResponse) -> Pricing:
        raise NotImplementedError

    def bind_pricing(self, pricing: AbstractPricingResponse) -> Pricing:
        return Pricing(list_price=pricing.list_price, sale_price=pricing.sale_price)





