from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.infrastructure.serbom.translators.serbom_product_translator import SerbomProductTranslator
from menu_sun_integration.infrastructure.serbom.presentations.product.serbom_product_get_request import \
    SerbomProductGetRequest
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.product.abstract_product_response import AbstractProductResponse
from menu_sun_integration.presentations.product.abstract_product_get_request import \
    AbstractProductGetRequest


class SerbomProductDefaultTranslator(SerbomProductTranslator):
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    def to_seller_get_format(self, seller: Seller, **kwargs) -> AbstractProductGetRequest:

        return SerbomProductGetRequest()

    def to_domain_format(self, response: AbstractProductResponse) -> [Product]:
        product = self.bind_product_or_bind_and_update_parameters(response)
        return product
