from menu_sun_api.domain.model.product.product import Product
from menu_sun_integration.application.translators.interfaces.abstract_inventory_translator import \
    AbstractInventoryTranslator
from menu_sun_integration.infrastructure.pernod.presentations.inventory.pernod_inventory_by_sku_post_request import \
    PernodInventoryBySkuPostRequest
from menu_sun_integration.infrastructure.pernod.presentations.inventory.pernod_inventory_response import \
    PernodInventoryResponse


class PernodInventoryTranslator(AbstractInventoryTranslator):
    def __init__(self):
        super().__init__()

    def bind_inventory(self, product: PernodInventoryResponse) -> Product:
        return Product(sku=product.sku, inventory=product.inventory, sale_price=product.sale_price,
                       list_price=product.sale_price)

    def to_seller_get_format(self, product: Product) -> PernodInventoryBySkuPostRequest:
        return PernodInventoryBySkuPostRequest(product.sku)

    def to_domain_format(self, response: PernodInventoryResponse) -> Product:
        return self.bind_inventory(response)
