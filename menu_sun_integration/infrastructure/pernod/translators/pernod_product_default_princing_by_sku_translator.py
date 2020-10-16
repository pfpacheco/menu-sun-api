from menu_sun_api.domain.model.product.product import Product
from menu_sun_integration.application.translators.interfaces.abstract_product_default_princing_by_sku_translator import \
    AbstractProductDefaultPricingBySkuTranslator
from menu_sun_integration.infrastructure.pernod.presentations.pricing.pernod_pricing_response import \
    PernodPricingResponse
from menu_sun_integration.infrastructure.pernod.presentations.pricing.product.\
    pernod_product_default_pricing_by_sku_post_request import \
    PernodProductDefaultPricingBySkuPostRequest


class PernodProductDefaultPricingBySkuTranslator(AbstractProductDefaultPricingBySkuTranslator):
    def __init__(self):
        super().__init__()

    def to_seller_get_format(self, product: Product) -> PernodProductDefaultPricingBySkuPostRequest:
        return PernodProductDefaultPricingBySkuPostRequest(product.sku)

    def to_domain_format(self, response: PernodPricingResponse) -> Product:
        return self.bind_prices(response)
