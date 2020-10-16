from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.adapters.interfaces.abstract_domain_adapter import AbstractDomainAdapter
from menu_sun_integration.application.adapters.interfaces.abstract_get_adapter import AbstractGetAdapter
from menu_sun_integration.application.clients.interfaces.abstract_product_client import AbstractProductClient
from menu_sun_integration.application.translators.interfaces.abstract_product_translator import \
    AbstractProductTranslator
from menu_sun_integration.presentations.product.abstract_product_get_response import AbstractProductGetResponse
from menu_sun_integration.presentations.product.abstract_product_response import AbstractProductResponse


class ProductAdapter(AbstractGetAdapter, AbstractDomainAdapter):
    def __init__(self, client: AbstractProductClient, translator: AbstractProductTranslator):
        self._client = client
        self._translator = translator

    def get_from_seller(self, seller: Seller) -> AbstractProductGetResponse:
        request = self._translator.to_seller_get_format(seller)
        return self._client.get_products(request)

    def get_domain(self, response: AbstractProductResponse) -> Product:
        return self._translator.to_domain_format(response)




