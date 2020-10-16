from menu_sun_api.domain.model.product.product import Product, ProductStatus
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.translators.interfaces.abstract_product_translator import \
    AbstractProductTranslator
from menu_sun_integration.infrastructure.pernod.presentations.product.pernod_product_get_request import \
    PernodProductGetRequest
from menu_sun_integration.infrastructure.pernod.presentations.product.pernod_product_response import \
    PernodProductResponse
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest


class PernodProductTranslator(AbstractProductTranslator):
    def bind_product(self, product: PernodProductResponse) -> Product:
        status = ProductStatus.ENABLED if product.active else ProductStatus.DISABLED
        return Product(status=status,
                       sku=product.sku, name=product.name, description=product.description, weight=product.weight,
                       ean=product.ean, brand=product.brand, width=product.width, height=product.height,
                       length=product.length)

    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        pass

    def to_seller_get_format(self, seller: Seller, **kwargs) -> PernodProductGetRequest:
        return PernodProductGetRequest()

    def to_domain_format(self, response: PernodProductResponse) -> [Product]:
        return self.bind_product(response)

