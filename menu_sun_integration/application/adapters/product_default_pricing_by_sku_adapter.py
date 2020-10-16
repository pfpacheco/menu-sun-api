from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.adapters.interfaces.abstract_domain_adapter import AbstractDomainAdapter
from menu_sun_integration.application.adapters.interfaces.abstract_get_adapter import AbstractGetAdapter
from menu_sun_integration.application.clients.interfaces.abstract_product_default_pricing_by_sku_client import \
    AbstractProductDefaultPricingBySkuClient
from menu_sun_integration.application.translators.interfaces.abstract_product_default_princing_by_sku_translator import\
    AbstractProductDefaultPricingBySkuTranslator
from menu_sun_integration.presentations.pricing.abstract_pricing_detail_get_response import \
    AbstractPricingDetailGetResponse
from menu_sun_integration.presentations.pricing.abstract_pricing_response import AbstractPricingResponse


class ProductDefaultPricingBySkuAdapter(AbstractGetAdapter, AbstractDomainAdapter):
    def __init__(self, client: AbstractProductDefaultPricingBySkuClient,
                 translator: AbstractProductDefaultPricingBySkuTranslator):
        self._client = client
        self._translator = translator

    def get_from_seller(self, product: Product) -> AbstractPricingDetailGetResponse:
        request = self._translator.to_seller_get_format(product)
        return self._client.get_price(request)

    def get_domain(self, response: AbstractPricingResponse) -> Product:
        return self._translator.to_domain_format(response)




