from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.translators.interfaces.abstract_product_translator import \
    AbstractProductTranslator
from menu_sun_integration.infrastructure.brf.presentations.product.brf_product_get_request import BRFProductGetRequest
from menu_sun_integration.infrastructure.brf.presentations.product.brf_product_response import BRFProductResponse
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest


class BRFProductTranslator(AbstractProductTranslator):
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    def to_seller_get_format(self, seller: Seller, **kwargs) -> BRFProductGetRequest:
        return BRFProductGetRequest()

    def to_domain_format(self, response: BRFProductResponse) -> [Product]:
        return self.bind_product(response)

