import abc

from menu_sun_integration.application.adapters.product_adapter import ProductAdapter
from menu_sun_integration.application.services.interfaces.abstract_service import AbstractService


class AbstractProductService(AbstractService):
    _adapter: ProductAdapter = None

    @abc.abstractmethod
    def update_products_from_seller(self) -> None:
        raise NotImplementedError
