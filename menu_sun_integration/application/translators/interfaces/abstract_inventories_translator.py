import abc

from menu_sun_api.domain.model.product.product import Product, ProductStatus
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.inventory.abstract_inventory_get_request import AbstractInventoryGetRequest
from menu_sun_integration.presentations.inventory.abstract_inventory_response import AbstractInventoryResponse


class AbstractInventoriesTranslator(AbstractTranslator):
    @abc.abstractmethod
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_seller_get_format(self, entity: Seller, **kwargs) -> AbstractInventoryGetRequest:
        raise NotImplementedError

    @abc.abstractmethod
    def to_domain_format(self, response: AbstractInventoryResponse) -> Product:
        raise NotImplementedError

    def bind_inventory(self, product: AbstractInventoryResponse) -> Product:
        return Product(sku=product.sku, inventory=product.inventory)
