import abc

from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.product.abstract_product_get_request import AbstractProductGetRequest
from menu_sun_integration.presentations.product.abstract_product_get_response import AbstractProductGetResponse


class AbstractProductClient(AbstractClient):
    @abc.abstractmethod
    def get_products(self, request: AbstractProductGetRequest) -> AbstractProductGetResponse:
        raise NotImplementedError
