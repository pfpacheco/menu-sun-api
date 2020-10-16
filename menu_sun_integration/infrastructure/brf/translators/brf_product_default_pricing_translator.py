from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.translators.interfaces.abstract_product_default_pricing_translator import \
    AbstractProductDefaultPricingTranslator
from menu_sun_integration.infrastructure.brf.presentations.pricing.brf_pricing_response import BRFPricingResponse
from menu_sun_integration.infrastructure.brf.presentations.pricing.product.\
    brf_product_default_pricing_detail_get_request import BRFProductDefaultPricingDetailGetRequest
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_detail_get_request import \
    AbstractProductDefaultPricingDetailGetRequest


class BRFProductDefaultPricingTranslator(AbstractProductDefaultPricingTranslator):
    def to_seller_send_format(self, entity: AbstractPlatform) -> AbstractRequest:
        raise NotImplementedError

    def to_seller_get_format(self, seller: Seller) -> AbstractProductDefaultPricingDetailGetRequest:
        metafield_postal_code = next(
            (field for field in seller.metafields if field.namespace == "INTEGRATION_API_FIELD"
             and field.key == "CDD_POSTAL_CODE"), None)

        postal_code = metafield_postal_code.value if metafield_postal_code else ""

        metafield_document = next(
            (field for field in seller.metafields if field.namespace == "INTEGRATION_API_FIELD"
             and field.key == "CDD_DOCUMENT"), None)

        document = metafield_document.value if metafield_document else ""

        return BRFProductDefaultPricingDetailGetRequest(document=document, postal_code=postal_code)

    def bind_pricing(self, pricing: BRFPricingResponse) -> Product:
        return Product(sku=pricing.sku, list_price=pricing.list_price, sale_price=pricing.sale_price,
                       promo_price=pricing.promo_price)

    def to_domain_format(self, response: BRFPricingResponse) -> [Product]:
        return self.bind_pricing(response)
