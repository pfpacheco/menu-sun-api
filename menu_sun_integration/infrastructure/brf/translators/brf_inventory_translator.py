from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.translators.interfaces.abstract_inventories_translator import \
    AbstractInventoriesTranslator
from menu_sun_integration.infrastructure.brf.presentations.inventory.brf_inventory_get_request import \
    BRFInventoryGetRequest
from menu_sun_integration.infrastructure.brf.presentations.inventory.brf_inventory_response import BRFInventoryResponse
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest


class BRFInventoryTranslator(AbstractInventoriesTranslator):
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    def to_seller_get_format(self, seller: Seller, **kwargs) -> BRFInventoryGetRequest:
        metafield_postal_code = next(
            (field for field in seller.metafields if field.namespace == "INTEGRATION_API_FIELD"
             and field.key == "CDD_POSTAL_CODE"), None)
        postal_code = metafield_postal_code.value if metafield_postal_code else ""

        return BRFInventoryGetRequest(postal_code=postal_code)

    def to_domain_format(self, response: BRFInventoryResponse) -> [Product]:
        return self.bind_inventory(response)

