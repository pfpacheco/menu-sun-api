import abc

from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator
from menu_sun_integration.presentations.inventory.abstract_inventory_by_sku_post_request import \
    AbstractInventoryBySkuPostRequest
from menu_sun_integration.presentations.inventory.abstract_inventory_response import AbstractInventoryResponse


class AbstractInventoryTranslator(AbstractTranslator):
    @abc.abstractmethod
    def to_seller_get_format(self, entity: Product) -> AbstractInventoryBySkuPostRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_domain_format(self, response: AbstractInventoryResponse) -> Product:
        raise NotImplementedError

    def bind_inventory(self, product: AbstractInventoryResponse) -> Product:
        return Product(sku=product.sku, inventory=product.inventory)
