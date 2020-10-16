import abc

from menu_sun_api.domain.model.product.product import Product, ProductStatus
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.product.abstract_product_get_request import AbstractProductGetRequest
from menu_sun_integration.presentations.product.abstract_product_response import AbstractProductResponse


class AbstractProductTranslator(AbstractTranslator):
    @abc.abstractmethod
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_seller_get_format(self, entity: Seller, **kwargs) -> AbstractProductGetRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_domain_format(self, response: AbstractProductResponse) -> Product:
        raise NotImplementedError

    def bind_product(self, product: AbstractProductResponse) -> Product:
        status = ProductStatus.ENABLED if product.active else ProductStatus.DISABLED
        return Product(status=status, sku=product.sku, name=product.name,
                       description=product.description, weight=product.weight, ean=product.ean, brand=product.brand)
