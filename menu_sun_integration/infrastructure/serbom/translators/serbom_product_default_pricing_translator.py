from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.translators.interfaces.abstract_product_default_pricing_translator import \
    AbstractProductDefaultPricingTranslator
from menu_sun_integration.infrastructure.serbom.presentations.pricing.product.\
    serbom_product_default_pricing_detail_get_request import \
    SerbomProductDefaultPricingDetailGetRequest
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.pricing.abstract_pricing_response import AbstractPricingResponse
from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_detail_get_request import \
    AbstractProductDefaultPricingDetailGetRequest


class SerbomProductDefaultPricingTranslator(AbstractProductDefaultPricingTranslator):
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    def to_seller_get_format(self, seller: Seller, **kwargs) -> AbstractProductDefaultPricingDetailGetRequest:

        return SerbomProductDefaultPricingDetailGetRequest()

    def to_domain_format(self, response: AbstractPricingResponse) -> [Product]:
        return self.bind_pricing(response)
