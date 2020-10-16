import abc

from menu_sun_api.domain.model.product.product import Product
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator
from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_by_sku_post_request import \
    AbstractProductDefaultPricingBySkuPostRequest
from menu_sun_integration.presentations.pricing.abstract_pricing_response import AbstractPricingResponse


class AbstractProductDefaultPricingBySkuTranslator(AbstractTranslator):
    @abc.abstractmethod
    def to_seller_get_format(self, entity: Product) -> AbstractProductDefaultPricingBySkuPostRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_domain_format(self, response: AbstractPricingResponse) -> Product:
        raise NotImplementedError

    def bind_prices(self, product: AbstractPricingResponse) -> Product:
        return Product(sku=product.sku, sale_price=product.sale_price, list_price=product.list_price)
