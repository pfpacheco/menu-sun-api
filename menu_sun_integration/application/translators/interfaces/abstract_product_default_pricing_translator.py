import abc

from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.pricing.abstract_pricing_response import AbstractPricingResponse
from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_detail_get_request import \
    AbstractProductDefaultPricingDetailGetRequest


class AbstractProductDefaultPricingTranslator(AbstractTranslator):
    @abc.abstractmethod
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_seller_get_format(self, seller: Seller) -> AbstractProductDefaultPricingDetailGetRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_domain_format(self, response: AbstractPricingResponse) -> Product:
        raise NotImplementedError

    def bind_pricing(self, pricing: AbstractPricingResponse) -> Product:
        return Product(sku=pricing.sku, list_price=pricing.list_price, sale_price=pricing.sale_price)





