from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.adapters.interfaces.abstract_domain_adapter import AbstractDomainAdapter
from menu_sun_integration.application.adapters.interfaces.abstract_get_adapter import AbstractGetAdapter
from menu_sun_integration.application.clients.interfaces.abstract_inventory_by_sku_client import \
    AbstractInventoryBySkuClient
from menu_sun_integration.application.translators.interfaces.abstract_inventory_translator import \
    AbstractInventoryTranslator
from menu_sun_integration.presentations.inventory.abstract_inventory_get_response import AbstractInventoryGetResponse
from menu_sun_integration.presentations.inventory.abstract_inventory_response import AbstractInventoryResponse


class InventoryAdapter(AbstractGetAdapter, AbstractDomainAdapter):
    def __init__(self, client: AbstractInventoryBySkuClient, translator: AbstractInventoryTranslator):
        self._client = client
        self._translator = translator

    def get_from_seller(self, product: Product) -> AbstractInventoryGetResponse:
        request = self._translator.to_seller_get_format(product)
        return self._client.get_inventory(request)

    def get_domain(self, response: AbstractInventoryResponse) -> Product:
        return self._translator.to_domain_format(response)




